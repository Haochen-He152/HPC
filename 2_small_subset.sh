#!/bin/bash
#BSUB -J simulate.py              
#BSUB -q hpc                      
#BSUB -W 0:10                     
#BSUB -n 1                        
#BSUB -R "span[hosts=1]"         
#BSUB -R "rusage[mem=4000]"      
#BSUB -R "select[model == XeonGold6126]"  
#BSUB -o Task_2/job_output_%J.out       
#BSUB -e Task_2/job_error_%J.err        

#number of floorplans to process
n=20

echo "Running simulate.py with n=$n"
start_time=$(date +%s.%N)  

# Save the result
python3 simulate.py $n >> Task_2/output_results.csv  

end_time=$(date +%s.%N)
runtime=$(echo "$end_time - $start_time" | bc)  

echo "Execution time: $runtime seconds"