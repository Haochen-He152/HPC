import sys
import numpy as np
import cupy as cp
import time
from os.path import join

def load_data_gpu(load_dir, bid):
    SIZE = 512
    # Load with numpy first
    u_cpu = np.zeros((SIZE + 2, SIZE + 2), dtype=np.float64)
    u_cpu[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask_cpu = np.load(join(load_dir, f"{bid}_interior.npy"))
    
    # Transfer to GPU
    u = cp.asarray(u_cpu)
    interior_mask = cp.asarray(interior_mask_cpu)
    return u, interior_mask

# Core fix: Fuse operations to eliminate temp arrays and launch overhead
@cp.fuse()
def fused_jacobi_step(u_up, u_down, u_left, u_right):
    return 0.25 * (u_up + u_down + u_left + u_right)

def jacobi_cupy_fixed(u, interior_mask, max_iter, atol):
    for i in range(max_iter):
        # Perform fused update
        u_new = fused_jacobi_step(
            u[:-2, 1:-1], 
            u[2:, 1:-1], 
            u[1:-1, :-2], 
            u[1:-1, 2:]
        )
        
        # Check convergence and update
        diff = cp.abs(u[1:-1, 1:-1][interior_mask] - u_new[interior_mask])
        delta = cp.max(diff)
        
        u[1:-1, 1:-1][interior_mask] = u_new[interior_mask]
        
        if delta < atol:
            break
    return u

def summary_stats_gpu(u, interior_mask):
    u_interior = u[1:-1, 1:-1][interior_mask]
    return {
        'mean_temp': float(cp.mean(u_interior)),
        'std_temp': float(cp.std(u_interior)),
        'pct_above_18': float(cp.sum(u_interior > 18) / u_interior.size * 100),
        'pct_below_15': float(cp.sum(u_interior < 15) / u_interior.size * 100),
    }

if __name__ == '__main__':
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    MAX_ITER = 20_000
    ABS_TOL = 1e-4
    
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()[:N]

    print(f"--- Running Task 10 Fix: CuPy FUSED on GPU for {N} buildings ---")
    
    stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    print('building_id, time_s, ' + ', '.join(stat_keys))

    for bid in building_ids:
        u, interior_mask = load_data_gpu(LOAD_DIR, bid)
        
        start_time = time.time()
        # Run fixed algorithm
        u_final = jacobi_cupy_fixed(u, interior_mask, MAX_ITER, ABS_TOL)
        cp.cuda.Stream.null.synchronize() # Wait for GPU to finish
        end_time = time.time()
        
        elapsed = end_time - start_time
        stats = summary_stats_gpu(u_final, interior_mask)
        
        res = [bid, f"{elapsed:.4f}"] + [str(stats[k]) for k in stat_keys]
        print(", ".join(map(str, res)))