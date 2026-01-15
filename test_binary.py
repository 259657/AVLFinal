import sys
from avl_binary import AVLTreeArray 
import os
import random

if __name__ == "__main__":

    tree = AVLTreeArray(capacity=10000)
    
    print(" AVL TREE (ARRAY) ")
    
    while True:
        print("\n === AVL MENU ===")
        print("1. Insert Node")
        print("2. Delete Node")
        print("3. Search Node")
        print("4. Show Tree ") 
        print("5. Save Tree to File (.png)")
        print("0. Exit")
        
        choice = input("\nSelect option: ")

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

                if tree.search_node(val) != -1:

                    tree.delete_node(val)
                    print(f"Deleted {val}")

                else:
                    print(f"Node {val} not found")

            except ValueError:
                print("Error: number needed")
           
        elif choice == '3':
            try:
                val = int(input("Enter integer to SEARCH: "))
                idx = tree.search_node(val)
                
                if idx != -1:
                    print(f"FOUND: Node {tree.tree[idx]} at Index [{idx}]")
                else:
                    print(f"Not found")
            except ValueError:
                print("Error: number needed")


         # VISUALIZATION 
        elif choice == '4':
  
  
            tree.visualize() 


        elif choice == '5':
            filename = input("Enter filename : ")
            if not filename.strip():
                filename = "my_tree"
            
            print(f"Save as '{filename}.png")
          
            tree.visualize(filename)



        elif choice == '0':
            print("Exit")
            break
        else:
            print("Try again")