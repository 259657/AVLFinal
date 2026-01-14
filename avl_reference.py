
import graphviz
import io               
from PIL import Image

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None
        print("init tree")


    def insert_node(self,key):
        self.root = self.insert(self.root, key)

    def insert(self, node, key):
            
        if not node:
            #print(f"Inserting {key} node")
            return Node(key)
        elif key < node.key:
            #print(f"{key} < {node.key}, going left from node {node.key}")
            node.left = self.insert(node.left,key)
        elif key > node.key:
            #print(f"{key} > {node.key}, going right from node {node.key}")
            node.right = self.insert(node.right, key)
        else:
            print(f"Duplicate: {key} already exists at node {node.key}")
            return node
        
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        balance = self.check_balance(node)

        # rotation
        #  Left Left
        if balance > 1 and key < node.left.key:
            return self.r_rotate(node)
        
        # Right Right 
        if balance < -1 and key > node.right.key:
            return self.l_rotate(node)
        
        #  Left Right 
        if balance > 1 and key > node.left.key:
            node.left = self.l_rotate(node.left)
            return self.r_rotate(node)
        
        #  Right Left
        if balance < -1 and key < node.right.key:
            node.right = self.r_rotate(node.right)
            return self.l_rotate(node)
        
        return node
            
    

    def delete_node(self, key):
        self.root = self.delete(self.root, key)

    def delete(self, node, key):
        if not node:
            return node
        if key < node.key:
            node.left = self.delete(node.left, key)
        elif key > node.key:
            node.right = self.delete(node.right, key)
        else:
            # node with one children or no children
          
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            #node with 2 childrens
           
            #PREDECESSOR
            temp = self.get_max_value_node(node.left)
            node.key = temp.key
            node.left = self.delete(node.left, temp.key)

           #SUCCESSOR
            # temp = self.get_min_value_node(node.right)
            # node.key = temp.key
            # #delete next
            # node.right = self.delete(node.right, temp.key)

        if not node:
            return node

        #  Update height
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        #  Balance
        balance = self.check_balance(node)
        # Left Left
        if balance > 1 and self.check_balance(node.left) >= 0:
            return self.r_rotate(node)

        # Left Right
        if balance > 1 and self.check_balance(node.left) < 0:
            node.left = self.l_rotate(node.left)
            return self.r_rotate(node)

        # Right Right
        if balance < -1 and self.check_balance(node.right) <= 0:
            return self.l_rotate(node)

        # Right Left
        if balance < -1 and self.check_balance(node.right) > 0:
            node.right = self.r_rotate(node.right)
            return self.l_rotate(node)

        return node

    def get_max_value_node(self, node):
        current = node
       
        while current.right is not None:
            current = current.right
        return current
    
    def get_min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def search_node(self, key):
        return self.search(self.root, key)
    

    def search(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self.search(node.left, key)
        return self.search(node.right, key)
    
    
    def r_rotate(self,x):
        y = x.left
        z = y.right

        #Rotation
        y.right = x
        x.left = z

        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y
    
    def l_rotate(self,x):
         y = x.right
         z = y.left

        #Rotation
         y.left = x
         x.right = z

         x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
         y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

         return y

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def check_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right) # HL- Hr
    
    def visualize(self, filename=None):
       
        dot = graphviz.Digraph(comment='AVL Tree')
        if self.root:
            self.add_nodes_edges(self.root, dot)
        
        if filename:
           
          
                dot.render(filename, view=True, format='png')
                print(f"Visualization saved as {filename}.png")
        else:
           
    
                png_bytes = dot.pipe(format='png')
                image = Image.open(io.BytesIO(png_bytes))
                image.show()
                print(" Displaying visualization")
            
    def add_nodes_edges(self, node, dot):
        if node:
            label = f"{node.key}\nh={node.height}"
            dot.node(str(node.key), label)
            
            if node.left:
                dot.edge(str(node.key), str(node.left.key), label='L')
                self.add_nodes_edges(node.left, dot)
            
            if node.right:
                dot.edge(str(node.key), str(node.right.key), label='R')
                self.add_nodes_edges(node.right, dot)
    

    
