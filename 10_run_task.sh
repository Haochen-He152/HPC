#!/bin/bash
#BSUB -J task10_nsys
#BSUB -q gpua40                   
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -W 0:15
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=8000]"
#BSUB -o Task_10/nsys_%J.out
#BSUB -e Task_10/nsys_%J.err

mkdir -p Task_10
rm -rf ~/.cupy/compiler_cache

# 1. 拿走工具：加载 CUDA，系统现在认识 nsys 了！
module load cuda

# 2. 激活你的 Python 环境
source /dtu/projects/02613_2025/conda/miniconda3/bin/activate 02613_2026

# 3. 屏蔽毒药（绝对核心）：强行让系统优先使用 Conda 内部的最新版 CUDA 库，无视刚才借出来的 11.8！
export LD_LIBRARY_PATH=/dtu/projects/02613_2025/conda/miniconda3/envs/02613_2026/lib:$LD_LIBRARY_PATH

N_BUILDINGS=2

echo -e "\n========================================================="
echo " Profiling Task 9: CuPy (The Problem - 未优化的原版) "
echo "========================================================="
nsys profile \
    --trace=cuda \
    --stats=true \
    --output=Task_10/profile_task9_unoptimized \
    --force-overwrite true \
    python3 9_cupy_jacobi.py $N_BUILDINGS

echo -e "\n========================================================="
echo " Profiling Task 10: CuPy Fused (The Fix - 融合优化版) "
echo "========================================================="
nsys profile \
    --trace=cuda \
    --stats=true \
    --output=Task_10/profile_task10_fused \
    --force-overwrite true \
    python3 10_fix.py $N_BUILDINGS

echo "Task 10 profiling finished!"