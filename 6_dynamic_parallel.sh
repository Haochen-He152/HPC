#!/bin/bash
#BSUB -J task6_dynamic             # Job name
#BSUB -q hpc                       # HPC queue
#BSUB -W 0:15                      # Wall time limit
#BSUB -n 24                        # Request 24 cores
#BSUB -R "span[hosts=1]"           # Single node constraint
#BSUB -R "rusage[mem=4000]"        # Memory per core
#BSUB -o Task_6/dynamic_%J.out     # Standard output log path
#BSUB -e Task_6/dynamic_%J.err     # Error log path

# Create Task_6 directory
mkdir -p Task_6

# Activate environment using specified source path
source /dtu/projects/02613_2025/conda/miniconda3/bin/activate 02613_2026

# Execution parameters
N=48
CORES=24

echo "Running dynamic parallel simulation for $N buildings with $CORES cores..."

# Start timing
start_time=$(date +%s.%N)

# Run python script and save results into Task_6 folder
python3 6_simulate_dynamic_parallel.py $N $CORES > Task_6/dynamic_results.csv

# End timing and calculate runtime
end_time=$(date +%s.%N)
runtime=$(echo "$end_time - $start_time" | bc)

echo "Finished. Total runtime: $runtime seconds"