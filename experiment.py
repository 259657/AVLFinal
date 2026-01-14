import time
import tracemalloc
import numpy as np
import os
import math
import matplotlib.pyplot as plt
import gc
import random


from avl_reference import AVLTree
from avl_binary import AVLTreeArray


MAX_N = 50000        
BATCH_SIZE = 1000    
PLOT_DIR = "plots_combined"
DATA_DIR = "datasets"


def get_dataset(n):
    
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    path = os.path.join(DATA_DIR, f"data_{n}.txt")
    
    if not os.path.exists(path):
        # Generate unique random numbers
        data = random.sample(range(1, n * 10), n)
        with open(path, 'w') as f:
            for num in data:
                f.write(f"{num}\n")
        return np.array(data)
    
    return np.loadtxt(path, dtype=int)


def run_batched_benchmark(tree_factory, data, delete_order, batch_size):
   
    results = {
        "x": [], 
        "insert_time": [],
        "search_time": [],
        "mem_static": [],    
        "mem_total": [],     
        "mem_growth": [],    
        "delete_x": [],      
        "delete_time": []
    }
    
    # Prepare batches
    total_items = len(data)
    insert_batches = [data[i:i + batch_size] for i in range(0, total_items, batch_size)]
    delete_batches = [delete_order[i:i + batch_size] for i in range(0, len(delete_order), batch_size)]
    
    current_size = 0
    
    # Setup memory tracking
    gc.collect()
    gc.enable()         
    tracemalloc.start()
    
    #  Init Tree
    tree = tree_factory()
    current_after_init, _ = tracemalloc.get_traced_memory()
    static_mb = current_after_init / (1024 * 1024)
    print(f"  -> Init done. Static Mem: {static_mb:.4f} MB")

    #  Growth Phase (Insert + Search)
    for batch in insert_batches:
        # Measure Insert
        t0 = time.perf_counter()
        for val in batch:
            tree.insert_node(val)
        t_insert = time.perf_counter() - t0
        
        current_size += len(batch)
        
        # Measure Memory
        current_mem, _ = tracemalloc.get_traced_memory()
        current_mb = current_mem / (1024 * 1024)
        growth_mb = current_mb - static_mb 
        
        # Measure Search
        search_sample = data[np.random.randint(0, current_size, size=len(batch))]
        t0 = time.perf_counter()
        for val in search_sample:
            tree.search_node(val)
        t_search = time.perf_counter() - t0
        
        # Record stats
        results["x"].append(current_size)
        results["insert_time"].append(t_insert)
        results["search_time"].append(t_search)
        results["mem_static"].append(static_mb)
        results["mem_total"].append(current_mb)
        results["mem_growth"].append(growth_mb)







    # Delete Phase
    delete_current_size = total_items
    
    for batch in delete_batches:
        t0 = time.perf_counter()
        for val in batch:
            tree.delete_node(val)
        t_delete = time.perf_counter() - t0
        
        results["delete_x"].append(delete_current_size)
        results["delete_time"].append(t_delete)
        delete_current_size -= len(batch)

    # Cleanup
    tracemalloc.stop()
    gc.collect()
    return results


def plot_comparison_on_one_chart(res_arr, res_ref, x_key, y_key, title, ylabel, filename, use_log=False):
    
    plt.figure(figsize=(10, 6))

    # Array AVL (Red)
    plt.plot(res_arr[x_key], res_arr[y_key], label='Array AVL', color='red', 
             marker='.', linestyle='-', linewidth=1.5, alpha=0.9)

    # Reference AVL (Blue)
    plt.plot(res_ref[x_key], res_ref[y_key], label='Reference AVL', color='blue', 
             marker='.', linestyle='-', linewidth=1.5, alpha=0.9)

    plt.title(title)
    plt.xlabel("N (Number of Elements)")
    plt.ylabel(ylabel)
    plt.legend() 
    plt.grid(True, linestyle='--', alpha=0.6)

    # if use_log:
    #     plt.yscale('log')
        
    path = os.path.join(PLOT_DIR, filename)
    plt.savefig(path)
    plt.close()
    print(f"Saved: {path}")


if __name__ == "__main__":
    os.makedirs(PLOT_DIR, exist_ok=True)
    
    print(f"Generating dataset N={MAX_N}...")
    data = get_dataset(MAX_N)
    
    # Prepare delete order ONCE to ensure consistency
    delete_order = np.copy(data)
    np.random.shuffle(delete_order)
    
    # Array AVL
    # Calc capacity based on log2(N) + buffer
    exponent = int(math.log2(MAX_N)) + 4
    capacity = 2 ** exponent
    print(f"\n[Array] Running Batches (Capacity: {capacity})")
    res_arr = run_batched_benchmark(
        lambda: AVLTreeArray(capacity=capacity), 
        data, 
        delete_order, 
        BATCH_SIZE
    )
    
    # Reference AVL
    print(f"\n[Reference] Running Batches")
    res_ref = run_batched_benchmark(
        lambda: AVLTree(), 
        data, 
        delete_order, 
        BATCH_SIZE
    )
    
    print("\nGenerating Plots...")
    
    #  Insert Time
    plot_comparison_on_one_chart(res_arr, res_ref, "x", "insert_time", 
                                 "Insert Time Comparison", "Time (s)", "compare_insert.png")
    
    #  Search Time
    plot_comparison_on_one_chart(res_arr, res_ref, "x", "search_time", 
                                 "Search Time Comparison", "Time (s)", "compare_search.png")
    
    #  Delete Time
    plot_comparison_on_one_chart(res_arr, res_ref, "delete_x", "delete_time", 
                                 "Delete Time Comparison", "Time (s)", "compare_delete.png")
    
    #  Total Memory
    plot_comparison_on_one_chart(res_arr, res_ref, "x", "mem_total", 
                                 "Total Memory Usage Comparison", "Memory (MB)", 
                                 "compare_memory_total.png", use_log=True)
    
    # 5. Memory Growth
    plot_comparison_on_one_chart(res_arr, res_ref, "x", "mem_growth", 
                                 "Dynamic Memory Growth Comparison", "Memory Increase (MB)", 
                                 "compare_memory_growth.png", use_log=False)

    print(f"\nDone. Plots saved in '{PLOT_DIR}'.")