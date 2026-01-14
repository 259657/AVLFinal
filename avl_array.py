
from array import array
import graphviz

class AVLTreeArray:
    def __init__(self, capacity=100000):
        self.capacity = capacity

        self.keys = array('i', [0] * capacity)
        self.left = array('i', [-1] * capacity)
        self.right = array('i', [-1] * capacity)
        self.height = array('i', [0] * capacity)
        
        self.root = -1      
        self.free_idx = 0  

    def new_node(self, key):
        if self.free_idx >= self.capacity:
            raise MemoryError("Memoty error")
        
        idx = self.free_idx
        self.free_idx += 1
        
        self.keys[idx] = int(key)
        self.left[idx] = -1
        self.right[idx] = -1
        self.height[idx] = 1
        return idx

    def insert_node(self, key):
        self.root = self.insert(self.root, key)

    def insert(self, node, key):
        if node == -1:
            return self.new_node(key)

        current_key = self.keys[node]
        
        if key < current_key:
            self.left[node] = self.insert(self.left[node], key)
        elif key > current_key:
            self.right[node] = self.insert(self.right[node], key)
        else:
            return node 
        
   
        self.height[node] = 1 + max(self.get_height(self.left[node]), self.get_height(self.right[node]))

        balance = self.check_balance(node)

    
        
        # Left Left
        left_child = self.left[node]
        if balance > 1 and key < self.keys[left_child]:
            return self.r_rotate(node)
        
        # Right Right
        right_child = self.right[node]
        if balance < -1 and key > self.keys[right_child]:
            return self.l_rotate(node)
        
        # Left Right
        if balance > 1 and key > self.keys[left_child]:
            self.left[node] = self.l_rotate(left_child)
            return self.r_rotate(node)
        
        # Right Left
        if balance < -1 and key < self.keys[right_child]:
            self.right[node] = self.r_rotate(right_child)
            return self.l_rotate(node)
        
        return node

    def delete_node(self, key):
        self.root = self.delete(self.root, key)

    def delete(self, node, key):
        if node == -1:
            return -1 
        
        current_key = self.keys[node]

        if key < current_key:
            self.left[node] = self.delete(self.left[node], key)
        elif key > current_key:
            self.right[node] = self.delete(self.right[node], key)
        else:
     
            left_child = self.left[node]
            right_child = self.right[node]

          
            if left_child == -1:
                return right_child
            elif right_child == -1:
                return left_child
            
         
           
            
            #PREDECESSOR
           
            temp = self.get_max_value_node(left_child) 
            self.keys[node] = self.keys[temp]
           
            self.left[node] = self.delete(left_child, self.keys[temp])

            #SUCCESSOR
           
            # temp = self.get_min_value_node(right_child) 
            # self.keys[node] = self.keys[temp]
            # self.right[node] = self.delete(right_child, self.keys[temp])

        if node == -1:
            return -1

   
        self.height[node] = 1 + max(self.get_height(self.left[node]), self.get_height(self.right[node]))

        # Balansowanie
        balance = self.check_balance(node)
        l = self.left[node]
        r = self.right[node]

        if balance > 1 and self.check_balance(l) >= 0:
            return self.r_rotate(node)

        if balance > 1 and self.check_balance(l) < 0:
            self.left[node] = self.l_rotate(l)
            return self.r_rotate(node)

        if balance < -1 and self.check_balance(r) <= 0:
            return self.l_rotate(node)

        if balance < -1 and self.check_balance(r) > 0:
            self.right[node] = self.r_rotate(r)
            return self.l_rotate(node)

        return node

 

    # PREDECESSOR
    def get_max_value_node(self, node):
        current = node
        while self.right[current] != -1:
            current = self.right[current]
        return current

    # SUCCESSOR 
    def get_min_value_node(self, node):
        current = node
        while self.left[current] != -1:
            current = self.left[current]
        return current
    

    def search_node(self, key):
     
        return self.search(self.root, key)

    def search(self, node, key):
        
        current_idx = node
        while current_idx != -1:
            current_val = self.keys[current_idx]
            
            if key == current_val:
                return current_idx  
            elif key < current_val:
                current_idx = self.left[current_idx]
            else:
                current_idx = self.right[current_idx]
        
        return -1  



    def r_rotate(self, x):
        y = self.left[x]
        z = self.right[y]

        self.right[y] = x
        self.left[x] = z

        self.height[x] = 1 + max(self.get_height(self.left[x]), self.get_height(self.right[x]))

        self.height[y] = 1 + max(self.get_height(self.left[y]), self.get_height(self.right[y]))
        return y

    def l_rotate(self, x):
        y = self.right[x]
        z = self.left[y]

        self.left[y] = x
        self.right[x] = z

        self.height[x] = 1 + max(self.get_height(self.left[x]), self.get_height(self.right[x]))
        self.height[y] = 1 + max(self.get_height(self.left[y]), self.get_height(self.right[y]))
        return y

    def get_height(self, node):
        if node == -1:
            return 0
        return self.height[node]

    def check_balance(self, node):
        if node == -1:
            return 0
        return self.get_height(self.left[node]) - self.get_height(self.right[node])

    def visualize(self, filename='avl_tree_array_final'):
        dot = graphviz.Digraph(comment='AVL Tree Array Module')
        if self.root != -1:
            self.add_nodes_edges(self.root, dot)
        try:
            dot.render(filename, view=True, format='png')
            print(f"Zapisano wizualizację: {filename}.png")
        except Exception as e:
            print(f"Błąd Graphviz: {e}")

    def add_nodes_edges(self, node, dot):
        if node != -1:
            k = self.keys[node]
            h = self.height[node]
            label = f"{k}\n(h={h})\n[idx={node}]"
            dot.node(str(node), label)
            
            l = self.left[node]
            r = self.right[node]
            
            if l != -1:
                dot.edge(str(node), str(l), label='L')
                self.add_nodes_edges(l, dot)
            
            if r != -1:
                dot.edge(str(node), str(r), label='R')
                self.add_nodes_edges(r, dot)