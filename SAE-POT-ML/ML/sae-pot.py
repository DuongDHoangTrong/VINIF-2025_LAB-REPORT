import os
import gc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import joblib
import argparse
import warnings
import tensorflow as tf
from tensorflow.keras import optimizers
from tensorflow.keras import backend as K
from tensorflow.keras import regularizers
from tensorflow.keras.callbacks import EarlyStopping, Callback, ReduceLROnPlateau, LearningRateScheduler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler
from sklearn.preprocessing import PolynomialFeatures

warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
tf.get_logger().setLevel('ERROR')

def run(model_name):
    model_name_0 = model_name + '_0'
    model_name_pic2para = 'pic2para'

    save_path = f'model/{model_name}'
    save_path_0 = f'model/{model_name_0}'
    save_path_pic2para = f'model/pic2para'

    NUM_FOLD = 5

    def LOSS(y_true, y_pred):
        LOSS1 = K.abs(y_pred - y_true)
        LOSS1 = K.mean(LOSS1, axis=-1)

        LOSS2 = K.square(y_pred - y_true)
        LOSS2 = K.mean(LOSS2, axis=-1)
        LOSS2 = K.sqrt(LOSS2)
        return tf.math.add(LOSS1, LOSS2)

    NxMax,Xmin,Xmax = 200, -20, +20
    NyMax,Ymin,Ymax = 100,   0, +20

    NxMax0,Xmin0,Xmax0 = 40, -4.6, +3.4
    NyMax0,Ymin0,Ymax0 = 10,  0.0, +2.0

    PARA_LIST = ['aH','sH','aC','sC','aN','sN']

    if model_name == 'pre_SAE':
        ENER_LIST, DIP_LIST, SYM_LIST = ['E_HOMO-2','E_HOMO-1','E_HOMO'], ['dx_HOMO-2','dx_HOMO-1','dx_HOMO'], ['s_HOMO']
    elif model_name == 'SAE':
        ENER_LIST, DIP_LIST, SYM_LIST = ['E_HOMO-2','E_HOMO-1','E_HOMO'], ['dx_HOMO-1','dx_HOMO'], ['s_HOMO']
    else:
        print('Check the model_name!')

    df = pd.read_csv(f'input.csv')
    COOR = df['pH']
    ENER = df[ENER_LIST]
    DIP = df[DIP_LIST]
    SYM = df[SYM_LIST]

    if (COOR > -2.45).any() or (COOR < -3.90).any():
        print('''WARNING: There exists a pH value outside the model's working range [-3.90;-2.45]. Prediction results may be misleading.''')

    if model_name == 'pre_SAE':
        X = pd.concat([ENER, DIP], axis=1)
    elif model_name == 'SAE':
        X = pd.concat([ENER, DIP, COOR], axis=1)
    else:
        print('Check the model_name!')
    X = X.to_numpy()

    def transform_data(data, save_path, model_name):
        poly = joblib.load(f'{save_path}/scaler/poly_{model_name}.joblib')
        scaler = joblib.load(f'{save_path}/scaler/scaler_{model_name}.joblib')
        pca = joblib.load(f'{save_path}/scaler/pca_{model_name}.joblib')

        data = poly.transform(data)
        data = scaler.transform(data)
        data = pca.transform(data)
        data = np.column_stack((data,SYM))
        return data

    def mirror(V):
        V1 = V[1:]
        V2 = V[:-1][::-1]
        return np.vstack((V1,V2))[::-1]

    X_0 = transform_data(X, save_path_0, model_name_0)
    predict_0 = {}
    for fold in range(NUM_FOLD):
        model = tf.keras.models.load_model(f'{save_path_0}/model/NN/final/{model_name_0}_fold{fold+1}.h5',
                                        custom_objects={'LOSS':LOSS}, compile=False)
        predict_0['fold_{}'.format(fold+1)] = model.predict(X_0, verbose=0)
        K.clear_session()

    X_ = transform_data(X, save_path, model_name)
    predict = {}
    for fold in range(NUM_FOLD):
        model = tf.keras.models.load_model(f'{save_path}/model/NN/final/{model_name}_fold{fold+1}.h5',
                                        custom_objects={'LOSS':LOSS}, compile=False)
        predict['fold_{}'.format(fold+1)] = model.predict(X_, verbose=0)
        K.clear_session()

    V_aver_0 = np.zeros((X.shape[0],NyMax0*NxMax0))
    for fold in range(NUM_FOLD):
        V_aver_0 += predict_0['fold_{}'.format(fold+1)]
    V_aver_0 /= NUM_FOLD
    V_aver_0 = V_aver_0.reshape(X.shape[0], NyMax0, NxMax0)

    V_aver = np.zeros((X.shape[0],NyMax*NxMax))
    for fold in range(NUM_FOLD):
        V_aver += predict['fold_{}'.format(fold+1)]
    V_aver /= NUM_FOLD

    Xstep=(Xmax-Xmin)/NxMax
    Ystep=(Ymax-Ymin)/NyMax
    a = round(abs(Xmin0-Xmin)/Xstep)
    b = round(abs(Ymax0-Ymax)/Ystep)
    for fold in range(NUM_FOLD):
        predict['fold_{}'.format(fold+1)].reshape((-1,NyMax,NxMax))[:,b:b+NyMax0,a:a+NxMax0]=predict_0['fold_{}'.format(fold+1)].reshape((-1,NyMax0,NxMax0))

    predict = {}
    para_aver = {}
    for i, label in enumerate(PARA_LIST):
        para_aver[label] = np.zeros((X.shape[0],1))
        for fold in range(NUM_FOLD):
            model = tf.keras.models.load_model(f'{save_path_pic2para}/model/NN/final/{model_name_pic2para}_{label}_fold{fold+1}.h5', compile=False)
            predict['{}-fold_{}'.format(label,fold+1)] = model.predict(V_aver_0, verbose=0)
            para_aver[label] += predict['{}-fold_{}'.format(label,fold+1)]

    for key in predict.keys():
        predict[key]=predict[key].flatten()
    pred_para_df = pd.DataFrame.from_dict(predict)

    for key in para_aver.keys():
        para_aver[key]=para_aver[key].flatten()
    aver_para_df = pd.DataFrame.from_dict(para_aver)/NUM_FOLD

    os.makedirs(f'output/para/', exist_ok = True)

    pred_para_df.to_csv(f'output/para/all_para.csv', index=False)
    aver_para_df.to_csv(f'output/para/aver_para.csv', index=False)

    os.makedirs(f'output/pic/', exist_ok = True)
    for i, V in enumerate(V_aver):
        posH = np.array(COOR)[i]
        V = mirror(V.reshape(NyMax,NxMax))
        np.savetxt('output/pic/{:.3f}-potential.in'.format(posH), V)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SAE-POT-ML')
    parser.add_argument('--model_name', type=str, default='SAE', help="model type")
    args = parser.parse_args()
    run(model_name=args.model_name)