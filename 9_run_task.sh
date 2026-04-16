#!/bin/bash
#BSUB -J task9_cupy                # Job name
#BSUB -q gpua40                   # GPU queue (Verified)
#BSUB -gpu "num=1:mode=exclusive_process" # Request 1 GPU
#BSUB -W 0:30                      # Wall time limit
#BSUB -n 4                         # Request 4 CPU cores per GPU (DTU rule)
#BSUB -R "span[hosts=1]"           # Single node constraint
#BSUB -R "rusage[mem=8000]"        # Memory allocation (8GB)
#BSUB -o Task_9/cupy_%J.out        # Output log
#BSUB -e Task_9/cupy_%J.err        # Error log

# Create output directory
mkdir -p Task_9

rm -rf ~/.cupy/compiler_cache


# Activate Conda environment
source /dtu/projects/02613_2025/conda/miniconda3/bin/activate 02613_2026

echo "========================================="
echo "        CuPy Environment Config          "
echo "========================================="

python3 -c "import cupy; cupy.show_config()"
echo "========================================="

#export LD_LIBRARY_PATH=/dtu/projects/02613_2025/conda/miniconda3/envs/02613_2026/lib:$LD_LIBRARY_PATH
# Test parameters
N_BUILDINGS=48

echo "Starting Task 9: CuPy implementation on GPU..."

# Run Python script and save to CSV format
python3 9_cupy_jacobi.py $N_BUILDINGS > Task_9/cupy_results.csv 2>&1

echo "Task 9 finished. Results in Task_9/cupy_results.csv"