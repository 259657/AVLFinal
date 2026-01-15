import cProfile
import pstats
import io
import numpy as np
import os
import math
import random

from avl_reference import AVLTree
from avl_binary import AVLTreeArray

MAX_N = 100000        
BATCH_SIZE = 1000    
DATA_DIR = "datasets"

# Profiling Checkpoints
CHECKPOINTS = [1000, 10000, 50000, 90000] 

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


def prepare_test_vectors(data, batch_size):

    print("Preparing test vector")
    total_items = len(data)
    
    #  Insert Batches 
    insert_batches = [data[i:i + batch_size] for i in range(0, total_items, batch_size)]
    
    #  Search Queries 
    search_queries = []
    current_data_pool = []

    
    for batch in insert_batches:
        current_data_pool.extend(batch)
        # Pick a random sample from the pool of currently inserted items
        sample_size = min(len(current_data_pool), batch_size)
        sample = np.random.choice(current_data_pool, size=sample_size, replace=False)
        search_queries.append(sample)
        
    # Delete Batches (Randomized order of all items)
    delete_order = np.copy(data)
    np.random.shuffle(delete_order)
    delete_batches = [delete_order[i:i + batch_size] for i in range(0, total_items, batch_size)]
    
    return insert_batches, search_queries, delete_batches


def run_profile_stats(name, func, *args):
  
    print(f"   >>> [PROFILER] {name}")
    pr = cProfile.Profile()
    pr.enable()
    
   
    func(*args)
    
    pr.disable()
    
    s = io.StringIO()
    # Sort stats by tottime time spent strictly inside the function excluding sub-calls
    ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
    ps.print_stats(10) 
    print(s.getvalue())


def run_profiled_benchmark(name, tree_factory, test_vectors):

    
    print(f"START PROFILING: {name}")
    
    
    insert_batches, search_queries, delete_batches = test_vectors
    tree = tree_factory()
    current_size = 0
    
    # INSERT + SEARCH
    for i, batch in enumerate(insert_batches):
        target_size = current_size + len(batch)
        
        # Check if adding this batch will hit a checkpoint
        should_profile = target_size in CHECKPOINTS
        
        if should_profile:
            print(f"\n[CHECKPOINT] Reaching N={target_size}...")
            
            #Profile INSERT
            def _op_insert():
                for val in batch: tree.insert_node(val)
            run_profile_stats("INSERT Batch", _op_insert)
            
            #Profile SEARCH
            queries = search_queries[i]
            def _op_search():
                for val in queries: tree.search_node(val)
            run_profile_stats("SEARCH Batch", _op_search)
            
        else:
            # Normal execution without profiling
            for val in batch:
                tree.insert_node(val)
                
        current_size += len(batch)

    # DELETE
    print(f"\nDELETING (Starting from N={current_size}) ---")
    
    for batch in delete_batches:
        # Check if CURRENT size (before deletion) matches a checkpoint
        should_profile = current_size in CHECKPOINTS
        
        if should_profile:
            print(f"\n[CHECKPOINT] Deleting from N={current_size}...")
            
            #Profile DELETE
            def _op_delete():
                for val in batch: tree.delete_node(val)
            run_profile_stats("DELETE Batch", _op_delete)
            
        else:
            # Normal execution without profiling
            for val in batch:
                tree.delete_node(val)
                
        current_size -= len(batch)


if __name__ == "__main__":
    print(f"Generating Data N={MAX_N}")
    data = get_dataset(MAX_N)
    
    # Prepare vectors
    vectors = prepare_test_vectors(data, BATCH_SIZE)
    
    # Profile Array AVL
    exponent = int(math.log2(MAX_N)) + 5
    capacity = 2 ** exponent
    print(f"\n[INIT] Array Capacity: {capacity}")
    
    run_profiled_benchmark("Array AVL", lambda: AVLTreeArray(capacity), vectors)
    
    # Profile Reference AVL
    run_profiled_benchmark("Reference AVL", lambda: AVLTree(), vectors)