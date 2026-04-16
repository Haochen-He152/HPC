import sys
import numpy as np
import time
from os.path import join
from numba import njit

# Numba optimized kernel
# fastmath=True allows the compiler to use aggressive optimizations
@njit(fastmath=True)
def jacobi_kernel(u, interior_mask, max_iter, atol):
    rows, cols = u.shape
    u_new = u.copy()
    
    iters_reached = max_iter
    for it in range(max_iter):
        delta = 0.0
        # Accessing memory in row-major order (i then j) for cache efficiency
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                # interior_mask indices are shifted by 1 relative to u
                if interior_mask[i-1, j-1]:
                    # Standard 5-point stencil update
                    val = 0.25 * (u[i-1, j] + u[i+1, j] + u[i, j-1] + u[i, j+1])
                    
                    diff = abs(u[i, j] - val)
                    if diff > delta:
                        delta = diff
                    u_new[i, j] = val
        
        # Update u for next iteration
        u[:] = u_new[:]
        
        if delta < atol:
            iters_reached = it + 1
            break
            
    return iters_reached

def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

def summary_stats(u, interior_mask):
    u_interior = u[1:-1, 1:-1][interior_mask]
    return {
        'mean_temp': u_interior.mean(),
        'std_temp': u_interior.std(),
        'pct_above_18': np.sum(u_interior > 18) / u_interior.size * 100,
        'pct_below_15': np.sum(u_interior < 15) / u_interior.size * 100,
    }

if __name__ == '__main__':
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    MAX_ITER = 20_000
    ABS_TOL = 1e-4

    # Run on a small subset (e.g., 10 buildings) as per Task 7a
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    
    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()[:N]

    stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    print('building_id, iters, time_s, ' + ', '.join(stat_keys))

    for bid in building_ids:
        u, interior_mask = load_data(LOAD_DIR, bid)
        
        start_time = time.time()
        iters = jacobi_kernel(u, interior_mask, MAX_ITER, ABS_TOL)
        end_time = time.time()
        
        elapsed = end_time - start_time
        stats = summary_stats(u, interior_mask)
        
        res = [bid, iters, f"{elapsed:.4f}"] + [str(stats[k]) for k in stat_keys]
        print(", ".join(map(str, res)))