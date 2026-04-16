#!/bin/bash
#BSUB -J task10_nsys               # Job name
#BSUB -q gpuv100                   # GPU queue
#BSUB -gpu "num=1:mode=exclusive_process" # Request 1 GPU
#BSUB -W 0:15                      # Wall time limit (15 mins is enough)
#BSUB -n 4                         # 4 CPU cores per GPU
#BSUB -R "span[hosts=1]"           # Single node constraint
#BSUB -R "rusage[mem=8000]"        # 8GB memory
#BSUB -o Task_10/nsys_%J.out       # Standard output log
#BSUB -e Task_10/nsys_%J.err       # Error log

# 1. Create directory for Task 10
mkdir -p Task_10

# 2. Load CUDA toolchain (Crucial for nsys)
module load cuda

# 3. Activate Conda environment
source /dtu/projects/02613_2025/conda/miniconda3/bin/activate 02613_2026

# Only process 2 buildings for profiling to keep the report file small
N_BUILDINGS=2

echo "========================================================="
echo " Profiling Task 8: Numba CUDA Kernel "
echo "========================================================="
# Run nsys for Task 8
# --trace=cuda: Only trace CUDA API and GPU workload
# --stats=true: Print summary statistics to the .out file
# --force-overwrite true: Overwrite if file already exists
nsys profile \
    --trace=cuda \
    --stats=true \
    --output=Task_10/profile_task8 \
    --force-overwrite true \
    python3 8_CUDA_streams.py $N_BUILDINGS

echo -e "\n\n========================================================="
echo " Profiling Task 9: CuPy Implementation "
echo "========================================================="
# Run nsys for Task 9
nsys profile \
    --trace=cuda \
    --stats=true \
    --output=Task_10/profile_task9 \
    --force-overwrite true \
    python3 9_cupy_jacobi.py $N_BUILDINGS

echo "Task 10 finished. Profiling reports are saved in Task_10/"