#!/bin/bash
#BSUB -J task12_run_all            # Job name
#BSUB -q gpua40                    # Verified Ampere queue
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -W 1:00                      # Wall time limit (1 hour should be plenty for GPU)
#BSUB -n 4                         # CPU cores
#BSUB -R "span[hosts=1]"           # Single node
#BSUB -R "rusage[mem=8000]"        # Memory allocation
#BSUB -o Task_12/run_all_%J.out    # Output log
#BSUB -e Task_12/run_all_%J.err    # Error log

mkdir -p Task_12

# Clear CuPy cache
rm -rf ~/.cupy/compiler_cache

# Activate Conda environment
source /dtu/projects/02613_2025/conda/miniconda3/bin/activate 02613_2026

N_BUILDINGS=5000

echo "Starting Task 12: Processing ALL buildings on GPU..."

# Run 10.fix.py
python3 10_fix.py $N_BUILDINGS > Task_12/all_results.csv 2>&1

echo "Task 12 computation finished. Results are saved in Task_12/all_results.csv"