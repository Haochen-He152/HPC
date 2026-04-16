#!/bin/bash
#BSUB -J profile_jacobi              
#BSUB -q hpc                      
#BSUB -W 0:15                     
#BSUB -n 1                        
#BSUB -R "span[hosts=1]"         
#BSUB -R "rusage[mem=4000]"      
#BSUB -R "select[model == XeonGold6126]"  

# The output path
#BSUB -o Task_4/task4_output_%J.out       
#BSUB -e Task_4/task4_error_%J.err        


#Activate the enviornment
source /dtu/projects/02613_2025/conda/miniconda3/bin/activate 02613_2026
KERNPROF=/dtu/projects/02613_2025/conda/miniconda3/envs/02613_2026/bin/kernprof

# Only calculate one building to record the profile
n=1
echo "Profiling jacobi function with n=$n"

# 2. Run kernprof and save as a file
kernprof -l -v 4_simulate_with_profile.py $n > Task_4/profiling_report.txt