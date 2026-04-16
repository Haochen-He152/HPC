#!/bin/bash
#BSUB -J task5_scaling            # Job name
#BSUB -q hpc                      # HPC queue
#BSUB -W 1:00                     # Wall time limit
#BSUB -n 24                       # Number of CPU cores
#BSUB -R "span[hosts=1]"          # Single node restriction
#BSUB -R "rusage[mem=4000]"       # Memory per core
#BSUB -o Task_5/scaling_%J.out    # Standard output log path
#BSUB -e Task_5/scaling_%J.err    # Error log path

# Create output directory
mkdir -p Task_5

# Activate conda environment
source /dtu/projects/02613_2025/conda/miniconda3/bin/activate 02613_2026

# Parameters for scaling test
N=48                              # Number of floorplans
cores_list=(1 2 4 8 12 24)        # List of core counts to test

# Prepare results file
RESULT_FILE="Task_5/speedup.csv"
echo "cores,time_seconds,speedup" > $RESULT_FILE

baseline_time=0

# Scaling test loop
for cores in "${cores_list[@]}"; do
    echo "Running with $cores cores..."

    start=$(date +%s.%N) # Record start time

    # Execute parallel simulation
    python3 5_simulate_parallel.py $N $cores > /dev/null

    end=$(date +%s.%N) # Record end time
    runtime=$(echo "$end - $start" | bc)

    # Compute speedup relative to 1-core baseline
    if [ "$cores" -eq 1 ]; then
        baseline_time=$runtime
        speedup=1.0
    else
        speedup=$(echo "scale=4; $baseline_time / $runtime" | bc)
    fi

    # Append results to CSV
    echo "$cores,$runtime,$speedup" >> $RESULT_FILE
done

echo "Test finished. Data saved to $RESULT_FILE"