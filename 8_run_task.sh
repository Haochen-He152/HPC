#!/bin/bash
#BSUB -J task8_gpu                 # Job name
#BSUB -q gpuv100                   # GPU queue 
#BSUB -gpu "num=1:mode=exclusive_process" # Request 1 GPU
#BSUB -W 0:30                      # Wall time limit
#BSUB -n 4                         # Single CPU core
#BSUB -R "rusage[mem=8000]"        # Memory allocation (8GB)
#BSUB -o Task_8/gpu_%J.out         # Standard output log
#BSUB -e Task_8/gpu_%J.err         # Error log

# Create output directory
mkdir -p Task_8


module load cuda
# Activate Conda environment
source /dtu/projects/02613_2025/conda/miniconda3/bin/activate 02613_2026

# Test parameters
N_BUILDINGS=48

echo "Starting Task 8: CUDA Numba Execution on GPU..."

# Run Python script
python3 8_CUDA_streams.py $N_BUILDINGS > Task_8/gpu_results.txt 2>&1

echo "Task 8 completed. Check Task_8/gpu_results.txt"