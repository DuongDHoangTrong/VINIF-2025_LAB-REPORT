import os
import numpy as np
import pandas as pd

file = open('temp.dat', 'r')
content0 = file.read()
file.close()

df = pd.read_csv('input.csv')

for i in range(df.shape[0]):
    content = content0

    for param, val in [('sC', df['sC'][i]),('aC', df['aC'][i]),
                       ('sH', df['sH'][i]),('aH', df['aH'][i]),
                       ('sN', df['sN'][i]),('aN', df['aN'][i]),
                       ('pH', df['pH'][i])]:
        content = content.replace('{'+param+'}', str(float(val)))
    
    path2param = '%i.dat' %i
    file = open(path2param,'w+')
    file.write(content)
    file.close()