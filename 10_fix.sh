#!/bin/bash
#BSUB -J task10_fix                # Job name
#BSUB -q gpua40                    # Verified Ampere queue
#BSUB -gpu "num=1:mode=exclusive_process" # Exclusive mode for accurate timing
#BSUB -W 0:30                      # Wall time limit
#BSUB -n 4                         # CPU cores
#BSUB -R "span[hosts=1]"           # Single node
#BSUB -R "rusage[mem=8000]"        # Memory allocation
#BSUB -o Task_10/fix_%J.out        # Output log
#BSUB -e Task_10/fix_%J.err        # Error log

# Create output directory
mkdir -p Task_10

# Clear CuPy cache
rm -rf ~/.cupy/compiler_cache

# Activate pure Conda environment
source /dtu/projects/02613_2025/conda/miniconda3/bin/activate 02613_2026

# Test all 48 buildings for fair comparison
N_BUILDINGS=48

echo "Starting Task 10 Fix: Running FUSED CuPy implementation..."

# Run fixed Python script
python3 10_fix.py $N_BUILDINGS > Task_10/fix_results.csv 2>&1

echo "Task 10 Fix finished. Results are saved in Task_10/fix_results.csv"