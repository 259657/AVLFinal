import sys
import os
import random

from avl_reference import AVLTree

if __name__ == "__main__":
    tree = AVLTree()
    
    print(" AVL TREE REFERENCE")
    
    while True:
        print("\n === AVL MENU (POINTERS) ===")
        print("1. Insert Node")
        print("2. Delete Node")
        print("3. Search Node")
        print("4. Show Tree ") 
        print("5. Save Tree to File (.png)")
        print("0. Exit")
        
        choice = input("\nSelect option: ")

        # INSERT
        if choice == '1':
            try:
                val = int(input("Enter integer to INSERT: "))
                tree.insert_node(val)
                print(f"Inserted {val}")
            except ValueError:
                print("Error: number needed")

        #  DELETE 
        elif choice == '2':
            try:
                val = int(input("Enter integer to DELETE: "))
              
                if tree.search_node(val):
                    tree.delete_node(val)
                    print(f"Deleted {val}")
                else:
                    print(f" Node {val} not found")
            except ValueError:
                print("Error: number needed")

        #  SEARCH 
        elif choice == '3':
            try:
                val = int(input("Enter integer to SEARCH: "))
                node = tree.search_node(val)
                if node:
                    print(f"FOUND Node {node.key} (Height: {node.height})")
                else:
                    print(f"Not found")
            except ValueError:
                print("Error: number needed")

        # VISUALIZATION 
        elif choice == '4':
            tree.visualize()

        #SAVE 
        elif choice == '5':
            filename = input("Enter filename : ")
            if not filename.strip():
                filename = "my_tree"
            
            print(f"Save as '{filename}.png'")
            tree.visualize(filename)
        elif choice == '6':
            try:
                n_str = input("Enter size of dataset (e.g. 20, 50): ")
                n = int(n_str)
                
  
                step_mode = input("Show step-by-step visualization? (y/n): ").lower()
                
                filepath = f"datasets2/data_{n}.txt"
                dataset = []

 
                if os.path.exists(filepath):
                    print(f"Loading from file: {filepath}")
                    with open(filepath, 'r') as f:
                        dataset = [int(line.strip()) for line in f]
                else:
                    print(f"File not found. Generating {n} random numbers")
                    dataset = random.sample(range(1, n * 10), n)

    
                print(f"Starting insertion of {len(dataset)} elements")
                
                for idx, val in enumerate(dataset):
                    tree.insert_node(val)
                    print(f"[{idx+1}/{n}] Inserted {val}")

      
                    if step_mode == 'y':
            
                        tree.visualize()
                        
                        
                        input(f"Press Enter to continue")

                print(f"\nAll {len(dataset)} elements inserted")
                
                
                if step_mode != 'y':
                    viz_now = input("Do you want to visualize FINAL tree? (y/n): ")
                    if viz_now.lower() == 'y':
                        tree.visualize("final_tree")

            except ValueError:
                print("Error: Please enter a valid integer")
            except Exception as e:
                print(f"An error occurred: {e}")


        #EXIT
        elif choice == '0':
            print("Exit")
            break
        else:
            print("Try again")