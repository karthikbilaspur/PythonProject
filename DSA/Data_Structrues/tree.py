class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if not self.root:
            self.root = Node(value)
        else:
            self._insert(self.root, value)

    def _insert(self, node, value):
        if value < node.value:
            if node.left:
                self._insert(node.left, value)
            else:
                node.left = Node(value)
        else:
            if node.right:
                self._insert(node.right, value)
            else:
                node.right = Node(value)

    def inorder(self):
        self._inorder(self.root)
        print()  # Newline for readability

    def _inorder(self, node):
        if node:
            self._inorder(node.left)
            print(node.value, end=" ")
            self._inorder(node.right)

    def preorder(self):
        self._preorder(self.root)
        print()  # Newline for readability

    def _preorder(self, node):
        if node:
            print(node.value, end=" ")
            self._preorder(node.left)
            self._preorder(node.right)

    def postorder(self):
        self._postorder(self.root)
        print()  # Newline for readability

    def _postorder(self, node):
        if node:
            self._postorder(node.left)
            self._postorder(node.right)
            print(node.value, end=" ")

    def search(self, value):
        return self._search(self.root, value)

    def _search(self, node, value):
        if not node:
            return False
        if value == node.value:
            return True
        elif value < node.value:
            return self._search(node.left, value)
        else:
            return self._search(node.right, value)

# Create a binary tree
bt = BinaryTree()
bt.insert(5)
bt.insert(3)
bt.insert(7)
bt.insert(2)
bt.insert(4)
bt.insert(6)
bt.insert(8)

# Perform traversals
print("Inorder traversal:")
bt.inorder()
print("Preorder traversal:")
bt.preorder()
print("Postorder traversal:")
bt.postorder()

# Search for a value
print("Is 6 in the tree?")
print(bt.search(6))
print("Is 9 in the tree?")
print(bt.search(9))