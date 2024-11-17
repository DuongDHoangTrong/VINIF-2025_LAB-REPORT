THIS MATERIAL IS PROVIDED AS IS, WITH ABSOLUTELY NO WARRANTY, EXPRESSED OR IMPLIED. ANY USE IS AT YOUR OWN RISK.
Duong D. Hoang-Trong, 2023-12-25
Email: hoangtrongdaiduong00@gmail.com

----------------------------------------------------------------------------------------------------

						SAE-POT PROGRAM  

 .----------------.  .----------------.  .----------------.   .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. | | .--------------. || .--------------. || .--------------. |
| |    _______   | || |      __      | || |  _________   | | | |   ______     | || |     ____     | || |  _________   | |
| |   /  ___  |  | || |     /  \     | || | |_   ___  |  | | | |  |_   __ \   | || |   .'    `.   | || | |  _   _  |  | |
| |  |  (__ \_|  | || |    / /\ \    | || |   | |_  \_|  | | | |    | |__) |  | || |  /  .--.  \  | || | |_/ | | \_|  | |
| |   '.___`-.   | || |   / ____ \   | || |   |  _|  _   | | | |    |  ___/   | || |  | |    | |  | || |     | |      | |
| |  |`\____) |  | || | _/ /    \ \_ | || |  _| |___/ |  | | | |   _| |_      | || |  \  `--'  /  | || |    _| |_     | |
| |  |_______.'  | || ||____|  |____|| || | |_________|  | | | |  |_____|     | || |   `.____.'   | || |   |_____|    | |
| |              | || |              | || |              | | | |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' | | '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'   '----------------'  '----------------'  '----------------' 
 
   ___     ___     ___               ___    ___    _____  
  / __|   /   \   | __|     o O O   | _ \  / _ \  |_   _|                                 _______________________________ 
  \__ \   | - |   | _|     o        |  _/ | (_) |   | |                            ╱|、  <Finally, I can publish the code|
  |___/   |_|_|   |___|   TS__[O]  _|_|_   \___/   _|_|_                         (˚ˎ 。7   \_____________________________/
_|"""""|_|"""""|_|"""""| {======|_| """ |_|"""""|_|"""""|                         |、˜  〵   
"`-0-0-'"`-0-0-'"`-0-0-'./o--000'"`-0-0-'"`-0-0-'"`-0-0-'                         じしˍ,)ノ  

----------------------------------------------------------------------------------------------------

DEPENDENCIES  
The program is written in Python and can be executed on both Linux and Windows.

----------------------------------------------------------------------------------------------------

MAIN PROGRAM FILES  
- sae_pot.py: Main program file.  

----------------------------------------------------------------------------------------------------

SAMPLE INPUT FILES  
input.csv - This file contains positions of H, energies, dipoles, and symmetries of MOs.

In the input.csv file:  
- Column 1: pH - Position of H (in atomic units), with the positions of C and N set to -0.949 and 1.236, respectively.
- Columns 2-5: E_HOMO-3 to E_HOMO - Required energies for HOMO-3 through HOMO.
- Columns 6-9: dx_HOMO-3 to dx_HOMO - Required dipoles for HOMO-3 through HOMO.
- Columns 10-13: s_HOMO-3 to s_HOMO - Required symmetries for HOMO-3 through HOMO (0 for antisymmetry and 1 for symmetry).
- Row 28: Sample data for HCN at equilibrium (values calculated with GAUSSIAN using the 6-311+g(2d,p) basis set).
- Remaining rows: Data for the position of H around the equilibrium position (values calculated similarly).

----------------------------------------------------------------------------------------------------

PROGRAM RUNNING MODE  

pre_SAE  
Uses machine-learning models trained for the equilibrium case (pH = -2.959) to construct an SAE_POT, describing energies, dipoles, and symmetries of MOs (HOMO, HOMO-1, HOMO-2).

SAE  
Uses models trained for a pH range of [-3.90, -2.45] to construct an SAE_POT, similarly describing energies, dipoles, and symmetries of the MOs.

----------------------------------------------------------------------------------------------------

RUNNING THE MAIN PROGRAM  
1. Enter the required values for energies, dipoles, and symmetries of MOs for the desired position of H (pH) in input.csv.
2. Run the code with one of the following commands:  
   - For SAE model: python sae-pot.py --model_name SAE.  
   - For pre_SAE model: python sae-pot.py --model_name pre_SAE.  

----------------------------------------------------------------------------------------------------

SAMPLE OUTPUT FILES  
- output/para/all_para.csv: Predictions for six potential parameters across five models.  
- output/para/aver_para.csv: Average predictions for the same six parameters.
- output/pic/<pH>-potential.in: Potential array image for H at position <pH>.  

----------------------------------------------------------------------------------------------------

WARNING  
1. The prediction for sH can be unstable, causing inaccuracy in the dipole of HOMO. Fine-tuning may be required for optimal SAE_POT.
2. The error for HOMO's dipole may exceed 20% near pH values around -3.90, even with tuning.

----------------------------------------------------------------------------------------------------