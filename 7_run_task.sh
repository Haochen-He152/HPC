#!/bin/bash
#BSUB -J task7_numba               # Job name
#BSUB -q hpc                       # HPC queue
#BSUB -W 0:30                      # Wall time limit (30 mins is plenty)
#BSUB -n 1                         # Single core only for JIT testing
#BSUB -R "rusage[mem=4000]"        # 4GB Memory
#BSUB -o Task_7/numba_%J.out       # Log file in Task_7 folder
#BSUB -e Task_7/numba_%J.err       # Error file in Task_7 folder

# Create Task_7 directory
mkdir -p Task_7

# Activate specified environment
source /dtu/projects/02613_2025/conda/miniconda3/bin/activate 02613_2026

# Task 7a: Run for a small subset (10 floorplans)
N_SUBSET=10

echo "Starting Task 7: Numba JIT version on 1 core..."

# Execute and save results
python3 7_numba_jacobi.py $N_SUBSET > Task_7/numba_results.csv

echo "Task 7 finished. Results are in Task_7/numba_results.csv"