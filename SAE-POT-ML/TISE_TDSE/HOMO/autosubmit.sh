read -p "Enter the number of H positions to calculate: " n

mkdir -p out_TISE
mkdir -p out_wf-HOMO
mkdir -p out_wf-HOMO-1
mkdir -p out_TDSE
mkdir -p out_HHG

chmod +x TISE
chmod +x TDSE

for ((i = 0; i <= n; i++))
do
    echo "==========================================================="
	mv ./$i.dat ./MOL.nml
    echo "Starting calculation for case #$i..."
    
    echo "Executing Time-Independent Schrödinger Equation (TISE)..."
	./TISE
    echo "TISE calculation completed successfully."
    
    echo "Executing Time-Dependent Schrödinger Equation (TDSE)..."
	./TDSE
    echo "TDSE calculation completed successfully."
	
	mv ./TISE.fort 		./out_TISE/$i-TISE.fort
	mv ./HCN_wf4.fort 	./out_wf-HOMO/$i-wf.fort
	mv ./HCN_wf3.fort 	./out_wf-HOMO-1/$i-wf.fort
	mv ./TDSE.fort 		./out_TDSE/$i-TDSE.fort
	mv ./HHG.fort  		./out_HHG/$i-HHG.fort

    echo "Case #$i completed."
done
