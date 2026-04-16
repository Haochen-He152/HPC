import sys
import numpy as np
import time
import math
from os.path import join
from numba import cuda

# GPU Core function
@cuda.jit
def jacobi_kernel(u, u_new, interior_mask):
    # Get thread coordinates in 2D grid
    i, j = cuda.grid(2)
    rows, cols = u.shape
    
    # Check boundaries
    if 1 <= i < rows - 1 and 1 <= j < cols - 1:
        if interior_mask[i-1, j-1]:
            # Standard 5-point stencil update
            u_new[i, j] = 0.25 * (u[i-1, j] + u[i+1, j] + u[i, j-1] + u[i, j+1])

# Load data function
def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2), dtype=np.float64)
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

if __name__ == '__main__':
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    MAX_ITER = 20_000
    ABS_TOL = 1e-4
    
    # Read building IDs
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()[:N]

    # Set CUDA grid and block sizes
    threads_per_block = (16, 16)
    blocks_per_grid_x = math.ceil(514 / threads_per_block[0])
    blocks_per_grid_y = math.ceil(514 / threads_per_block[1])
    blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

    print(f"--- Processing {N} buildings on GPU ---")
    print(f"Grid size: {blocks_per_grid}, Block size: {threads_per_block}")

    # Task 8a: Measure kernel execution time & memory bandwidth
    print("\n[Task 8a] Measuring pure kernel performance...")
    u_host, mask_host = load_data(LOAD_DIR, building_ids[0])
    
    # Transfer data to GPU
    d_u = cuda.to_device(u_host)
    d_u_new = cuda.to_device(u_host)
    d_mask = cuda.to_device(mask_host)
    
    cuda.synchronize() 
    start_kernel = time.time()
    
    # Run fixed iterations for timing
    for _ in range(1000): 
        jacobi_kernel[blocks_per_grid, threads_per_block](d_u, d_u_new, d_mask)
        jacobi_kernel[blocks_per_grid, threads_per_block](d_u_new, d_u, d_mask)
        
    cuda.synchronize() 
    end_kernel = time.time()
    
    kernel_time = end_kernel - start_kernel
    print(f"Kernel execution time (2000 iters): {kernel_time:.4f} s")
    
    # Estimate memory bandwidth
    bytes_per_iter = (512 * 512) * 16 
    total_gb = (bytes_per_iter * 2000) / (1024**3)
    bandwidth = total_gb / kernel_time
    print(f"Estimated memory bandwidth: {bandwidth:.2f} GB/s")

    # Task 8b: CUDA Streams for concurrency
    print("\n[Task 8b] Running with CUDA Streams...")
    NUM_STREAMS = 4
    streams = [cuda.stream() for _ in range(NUM_STREAMS)]
    
    start_streams = time.time()
    
    for i, bid in enumerate(building_ids):
        stream = streams[i % NUM_STREAMS]
        
        # Load and transfer data in stream
        u, mask = load_data(LOAD_DIR, bid)
        d_u = cuda.to_device(u, stream=stream)
        d_u_new = cuda.to_device(u, stream=stream)
        d_mask = cuda.to_device(mask, stream=stream)
        
        # Execute kernel asynchronously
        for _ in range(1000):
            jacobi_kernel[blocks_per_grid, threads_per_block, stream](d_u, d_u_new, d_mask)
            jacobi_kernel[blocks_per_grid, threads_per_block, stream](d_u_new, d_u, d_mask)

    # Synchronize all streams
    cuda.synchronize()
    end_streams = time.time()
    
    total_time = end_streams - start_streams
    print(f"Total time for {N} buildings (Streaming): {total_time:.4f} s")