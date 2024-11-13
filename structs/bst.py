
class Node:
    
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        

class BST:
    
    def __init__(self):
        self.root = None
        
    def add_node(self, val):
        if self.root is None:
            self.root = Node(val)
        else:
            self.insert(self.root, val)
    
    def insert(self, node: Node, val: int) -> None:
        if node.val < val:
            if node.right is None:
                node.right = Node(val)
            else:
                self.insert(node.right, val)
        else:
            if node.left is None:
                node.left = Node(val)
            else:
                self.insert(node.left, val)
            
    def search(self, key) -> bool:
        return self.rec_search(self.root, key)

    def rec_search(self, node: Node, key: int) -> int:
        if node.val == key:
            return True

        elif node is None:
            return False
        
        elif key < node.val:
            return self.rec_search(node.left, key)
        
        else:
            return self.rec_search(node.right, key)
        
    def inorder(self):
        return self.inorder_dfs(self.root)
    
    def inorder_dfs(self, node):
        res = []
        if node:
            res = self.inorder_dfs(node.left)
            res.append(node.val)
            res += self.inorder_dfs(node.right)
            
        return res
    
    def remove(self, key):
        self.root = self._remove(self.root, key)

    def _remove(self, node, key):
        if node is None:
            return node

        if key < node.val:
            node.left = self._remove(node.left, key)
        elif key > node.val:
            node.right = self._remove(node.right, key)
        else:
            # Node with only one child or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            temp = self._minValueNode(node.right)

            node.val = temp.val

            node.right = self._remove(node.right, temp.val)

        return node

    def _minValueNode(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    
def main():
    bst = BST()
    values = [15, 10, 20, 8, 12, 16, 25]
    for value in values:
        bst.add_node(value)

    print("Inorder traversal of the BST before removal:")
    print(bst.inorder())
    
    bst.remove(8)
    print("Inorder traversal after removing a leaf node (8):")
    print(bst.inorder())

    bst.remove(15)
    print("Inorder traversal after removing a node with two children (15):")
    print(bst.inorder())

if __name__ == "__main__":
    main()