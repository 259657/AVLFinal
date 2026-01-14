# instruction 

# Istall all dependencies and active virtual envairement
python3 -m venv venv
source venv/bin/activate
cd avl
pip install -r requirements.txt
## Impementaion :

In file avl_reference.py is implementation of reference-based

In file avl_binary.py is implementation of array-based

## Visualization check Insertion/Delete/search

In files test.reference.py and test_binar.py after run you can create tree from scratch and visualize all steps by terminal and choose option what you want:
Insert/Delete/Search/Show/Save

## Dataset

The dictionary "datasets" contains sets of data where each file store random unique intiger

## Beanchmark

The file experiment.py contains the benchmarking used to evaluate the performance of AVL tree operations and plts all resoults
For a selected dataset, the script measures the execution time of insertion, deletion, and search operations
Experiments are performed in batches of 1,000 elements, allowing performance trends to be observed as the tree size grows

The file profile.py contains the internal profiling tools. The script analyzes the CPU time distribution across individual function calls at specific tree size checkpoints (e.g., N=50,000, N=90,000). This detailed analysis helps pinpoint expensive internal operations, such as data shifting in the array-based implementation versus pointer updates in the reference model