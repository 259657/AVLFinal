
import numpy as np
import graphviz
import io               
from PIL import Image

class AVLTreeArray:
    NIL = -1

    def __init__(self, capacity=100000):
        self.capacity = capacity

        self.tree = np.full(capacity, self.NIL, dtype=np.int32)
        self.height = np.zeros(capacity, dtype=np.int16)

        self.root = 0
    def left(self, i):
        return 2 * i + 1

    def right(self, i):
        return 2 * i + 2

    def val(self, i):
        if i >= self.capacity:
            return None
        v = self.tree[i]
        return None if v == self.NIL else v

    
    # BALANS
    
    def get_height(self, i):
        if i >= self.capacity or self.tree[i] == self.NIL:
            return 0
        return self.height[i]

    def update_height(self, i):
        self.height[i] = 1 + max(
            self.get_height(self.left(i)),
            self.get_height(self.right(i))
        )

    def balance(self, i):
        return self.get_height(self.left(i)) - self.get_height(self.right(i))


    # INSERT

    def insert_node(self, key):
        self.insert(self.root, int(key))

    def insert(self, i, key):
        if i >= self.capacity:
            raise RuntimeError("Tree capacity exceeded")

        if self.tree[i] == self.NIL:
            self.tree[i] = key
            self.height[i] = 1
            return i
        
        # going left
        if key < self.tree[i]:
            self.insert(self.left(i), key)
        # going right
        elif key > self.tree[i]:
            self.insert(self.right(i), key)
        else:
            print(f"Duplicate key found: {key}")
            return i # Duplicate

        self.update_height(i)
        b = self.balance(i)

        # AVL ROTATIONS 

        # Left Left
        if b > 1:
            if self.balance(self.left(i)) >= 0:
                return self.rotate_right(i)
        # Left Right
            else:
                self.rotate_left(self.left(i))
                return self.rotate_right(i)
        # Right Right
        if b < -1:
            if self.balance(self.right(i)) <= 0:
                return self.rotate_left(i)
        # Right Left
            else:
                self.rotate_right(self.right(i))
                return self.rotate_left(i)

        return i

 
    # DELETE
   
    def delete_node(self, key):
        self.delete(self.root, key)

    def delete(self, i, key):
        if self.val(i) is None:
            return i

        if key < self.tree[i]:
            self.delete(self.left(i), key)
        elif key > self.tree[i]:
            self.delete(self.right(i), key)
        else:
            # node with one children or no children
            l = self.left(i)
            r = self.right(i)

           
            
            if self.val(l) is None and self.val(r) is None:
                # no children
                self.tree[i] = self.NIL
                self.height[i] = 0
                return i

            elif self.val(l) is None:
                # only right children
                succ = self.min_node(r)
                self.tree[i] = self.tree[succ]
                self.delete(r, self.tree[succ])

            elif self.val(r) is None:

                #only left children
                pred = self.max_node(l)
                self.tree[i] = self.tree[pred]
                self.delete(l, self.tree[pred])

            else:
                # node with 2 childrens
                # PREDECESSOR
                temp = self.max_node(l)           
                self.tree[i] = self.tree[temp]    
                self.delete(l, self.tree[temp])   

        if self.tree[i] == self.NIL:
            return i

        # Update height
        self.update_height(i)
        
        # Balance
        b = self.balance(i)

        # Left Left
        if b > 1:
            if self.balance(self.left(i)) >= 0:
                return self.rotate_right(i)
            # Left Right
            else:
                self.rotate_left(self.left(i))
                return self.rotate_right(i)

        # Right Right
        if b < -1:
            if self.balance(self.right(i)) <= 0:
                return self.rotate_left(i)
            # Right Left
            else:
                self.rotate_right(self.right(i))
                return self.rotate_left(i)

        return i

    def min_node(self, i):

        while self.val(self.left(i)) is not None:

            i = self.left(i)

        return i

    def max_node(self, i):

        while self.val(self.right(i)) is not None:

            i = self.right(i)

        return i


    # Rotate 

    def rotate_left(self, i):

        subtree = self.extract(i)

        rotated = self.logic_rotate_left(subtree)

        self.clear(i)

        self.write(rotated, i)

        return i

    def rotate_right(self, i):

        subtree = self.extract(i) # tuple


        rotated = self.logic_rotate_right(subtree) #new tuple


        self.clear(i)


        self.write(rotated, i)
        return i


    # EXTRACT / CLEAR / WRITE

    def extract(self, i):
        # Recursively extract the subtree rooted at index i
        if self.val(i) is None:
            return None
        # start - where balance is incorected
        # (Parent, LeftChild, RightChild)
        return (
            self.tree[i],
            self.extract(self.left(i)),
            self.extract(self.right(i))
        )

    def clear(self, i):
         # Recursively clear the subtree rooted at index i
        if self.val(i) is None:
            return
        self.tree[i] = self.NIL
        self.height[i] = 0
        self.clear(self.left(i))
        self.clear(self.right(i))

    def write(self, node, i):
        # Recursively write a subtree 
        # back into the array using complete binary tree indexing
        if node is None:
            return
        if i >= self.capacity:
            raise RuntimeError("Rotation overflow")

        self.tree[i] = node[0]
        self.write(node[1], self.left(i))
        self.write(node[2], self.right(i))
        self.update_height(i)



    # LOGIC ROTATIONS 
    # y = (VAL, LEFT, RIGHT)
    def logic_rotate_right(self, y):
        x = y[1]
        z = x[2]
        return (x[0], x[1], (y[0], z, y[2]))

    def logic_rotate_left(self, x):
        y = x[2]
        z = y[1]
        return (y[0], (x[0], x[1], z), y[2])
            #new root  new left child   #new right child



    # SEARCH
 
    def search_node(self, key):
        return self.search(self.root, key)

    def search(self, i, key):
        if i >= self.capacity or self.tree[i] == self.NIL:
            return -1
        if self.tree[i] == key:
            return i
        if key < self.tree[i]:
            return self.search(self.left(i), key)
        return self.search(self.right(i), key)

    
    # VISUALIZATION
   
    def visualize(self, filename=None):
       
        dot = graphviz.Digraph(comment="Array-Based AVL Tree")
        self.viz(self.root, dot)
        
        if filename:
                dot.render(filename, view=True, format="png")
                print(f"Visualization saved as {filename}.png")
           
        else:
           
                png_bytes = dot.pipe(format='png')
                image = Image.open(io.BytesIO(png_bytes))
                image.show()
                

    def viz(self, i, dot):
        if self.val(i) is None:
            return
        dot.node(str(i), f"{self.tree[i]}\nh={self.height[i]}\n[{i}]")
        if self.val(self.left(i)) is not None:
            dot.edge(str(i), str(self.left(i)), "L")
            self.viz(self.left(i), dot)
        if self.val(self.right(i)) is not None:
            dot.edge(str(i), str(self.right(i)), "R")
            self.viz(self.right(i), dot)