THIS MATERIAL IS PROVIDED AS IS, WITH ABSOLUTELY NO WARRANTY, EXPRESSED OR IMPLIED. ANY USE IS AT YOUR OWN RISK.
Duong D. Hoang-Trong, 2024-10-20
Email: hoangtrongdaiduong00@gmail.com

----------------------------------------------------------------------------------------------------
  _______ _____  _____ ______            _______ _____   _____ ______ 
 |__   __|_   _|/ ____|  ____|   ___    |__   __|  __ \ / ____|  ____|
    | |    | | | (___ | |__     ( _ )      | |  | |  | | (___ | |__   
    | |    | |  \___ \|  __|    / _ \/\    | |  | |  | |\___ \|  __|  
    | |   _| |_ ____) | |____  | (_>  <    | |  | |__| |____) | |____ 
    |_|  |_____|_____/|______|  \___/\/    |_|  |_____/|_____/|______|
                                                                      
----------------------------------------------------------------------------------------------------

NOTE
This description applies to both the HOMO and HOMO-1 folders, which include code for solving
TISE and TDSE equations for HOMO and HOMO-1, respectively.

----------------------------------------------------------------------------------------------------

DEPENDENCIES  
The program is written in Fortran and packed that can be executed on both Linux and Windows.

----------------------------------------------------------------------------------------------------

MAIN PROGRAM FILES
- TISE: program solving TISE
- TDSE: program solving TDSE    

----------------------------------------------------------------------------------------------------

SAMPLE INPUT FILES  
input.csv - This file contains the positions of H and the potential parameters predicted by the SAE-POT-ML model.
INPUT.nml - This file contains variables for solving TISE, TDSE, and laser parameters (details provided below).

=======================================================================================================================	  
Variable      Type      Meaning 														
-----------------------------------------------------------------------------------------------------------------------
For laser  (Envelope type of laser is ’sin2’)
-----------------------------------------------------------------------------------------------------------------------
theta         real      Orientation                (degree)
I0            real      Intensity                  (10x14 W/cm2)
L0            real      Wavelength                 (nm)
w0            real      Frequency                  (a.u.)
cep           real      Carrier-envelope phase     (radian)
Np            real      Number of optical cycles				 	
=======================================================================================================================

----------------------------------------------------------------------------------------------------

RUNNING THE MAIN PROGRAM  
1. Enter the position of H and potential parameters (predicted by the SAE-POT-ML model) in input.csv.
2. Define all cases of potential paramters using the following commands:  
   - python initial.py  
3. Run the TISE and TDSE calculations for each case one by one using the following commands
   (note: this process may take some time):
   - source autosubmit.sh

----------------------------------------------------------------------------------------------------

OUTPUT FILES   
- out_TISE/<i>-TISE.fort: TISE calculations results for case <i> (including energies, dipoles - details in file).
- out_wf-HOMO/<i>-wf.fort: wave function of HOMO for case <i> (presented as a matrix).
- out_wf-HOMO-1/<i>-wf.fort: wave function of HOMO for case <i> (presented as a matrix).
- out_TDSE/<i>-TDSE.fort: TDSE calculations results for case <i> (including external electric field, electron’s acceleration, ionization probability - details in file).
- out_HHG/<i>-HHG.fort: HHG spectra for case <i> (including orders, intensity and phase - details in file). 

----------------------------------------------------------------------------------------------------
