"""
Data Structures - All in One File
==================================
Contains: Dictionary, Graph, LinkedList, List, Queue, Set, BinaryTree, Tuple
Run:  python index.py
"""

from typing import Any, Dict, List as TypingList, Optional


# ----------------------------------------------------------------------
# 1. DICTIONARY
# ----------------------------------------------------------------------
class Dictionary:
    def __init__(self):
        self.data: dict[str, Any] = {}

    def add(self, key: str, value: Any):
        self.data[key] = value

    def get(self, key: str) -> Any:
        return self.data.get(key)

    def update(self, key: str, value: Any) -> None:
        if key in self.data:
            self.data[key] = value
        else:
            print("Key not found")

    def delete(self, key: str) -> None:
        if key in self.data:
            del self.data[key]
        else:
            print("Key not found")

    def print_dict(self) -> None:
        for key, value in self.data.items():
            print(f"{key}: {value}")

    def sort_by_keys(self) -> dict[str, Any]:
        return dict(sorted(self.data.items()))

    def sort_by_values(self) -> dict[str, Any]:
        return dict(sorted(self.data.items(), key=lambda item: item[1]))


def demo_dictionary():
    print("\n--- Dictionary ---")
    d = Dictionary()
    d.add("apple", 5)
    d.add("banana", 10)
    d.add("cherry", 3)
    d.add("date", 8)
    print("Dictionary:")
    d.print_dict()
    print("\nGet value of 'apple':")
    print(d.get("apple"))
    d.update("apple", 6)
    print("\nUpdated dictionary:")
    d.print_dict()
    d.delete("banana")
    print("\nDictionary after deletion:")
    d.print_dict()
    print("\nDictionary sorted by keys:")
    print(d.sort_by_keys())
    print("\nDictionary sorted by values:")
    print(d.sort_by_values())


# ----------------------------------------------------------------------
# 2. GRAPH
# ----------------------------------------------------------------------
class Graph:
    def __init__(self):
        self.data: Dict[str, TypingList[str]] = {}

    def add_node(self, node: str):
        if node not in self.data:
            self.data[node] = []

    def add_edge(self, node1: str, node2: str):
        if node1 in self.data and node2 in self.data:
            self.data[node1].append(node2)
            self.data[node2].append(node1)

    def print_graph(self):
        for node in self.data:
            print(node, "->", self.data[node])

    def dfs(self, start_node: str) -> None:
        visited: set[str] = set()
        self._dfs_helper(start_node, visited)
        print()

    def _dfs_helper(self, node: str, visited: set[str]) -> None:
        visited.add(node)
        print(node, end=" ")
        for neighbor in self.data[node]:
            if neighbor not in visited:
                self._dfs_helper(neighbor, visited)

    def bfs(self, start_node: str) -> None:
        visited: set[str] = set()
        queue = [start_node]
        visited.add(start_node)
        while queue:
            node = queue.pop(0)
            print(node, end=" ")
            for neighbor in self.data[node]:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
        print()


def demo_graph():
    print("\n--- Graph ---")
    g = Graph()
    for n in ["A", "B", "C", "D", "E"]:
        g.add_node(n)
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("C", "E")
    g.add_edge("D", "E")
    print("Graph:")
    g.print_graph()
    print("\nDFS Traversal:")
    g.dfs("A")
    print("\nBFS Traversal:")
    g.bfs("A")


# ----------------------------------------------------------------------
# 3. LINKED LIST
# ----------------------------------------------------------------------
class Node:
    def __init__(self, data: int):
        self.data = data
        self.next: Optional['Node'] = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data: int):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def print_list(self):
        current = self.head
        while current:
            print(current.data, end=" ")
            current = current.next
        print()

    def sort(self):
        current = self.head
        while current:
            next_node = current.next
            while next_node:
                if current.data > next_node.data:
                    current.data, next_node.data = next_node.data, current.data
                next_node = next_node.next
            current = current.next


def demo_linked_list():
    print("\n--- Linked List ---")
    ll = LinkedList()
    for v in [64, 34, 25, 12, 22, 11, 90]:
        ll.append(v)
    print("Linked List:")
    ll.print_list()
    ll.sort()
    print("Sorted Linked List:")
    ll.print_list()


# ----------------------------------------------------------------------
# 4. LIST (Array List)
# ----------------------------------------------------------------------
class List:
    def __init__(self):
        self.data: TypingList[Any] = []

    def append(self, value: Any):
        self.data.append(value)

    def insert(self, index: int, value: Any):
        self.data.insert(index, value)

    def delete(self, index: int):
        if index < len(self.data):
            del self.data[index]
        else:
            print("Index out of range")

    def get(self, index: int):
        if index < len(self.data):
            return self.data[index]
        else:
            print("Index out of range")

    def update(self, index: int, value: Any):
        if index < len(self.data):
            self.data[index] = value
        else:
            print("Index out of range")

    def print_list(self):
        print(self.data)

    def sort(self):
        self.data.sort()

    def reverse(self):
        self.data.reverse()


def demo_list():
    print("\n--- List ---")
    l = List()
    for v in [5, 10, 3, 8]:
        l.append(v)
    print("List:")
    l.print_list()
    l.insert(2, 7)
    print("List after insertion:")
    l.print_list()
    l.delete(1)
    print("List after deletion:")
    l.print_list()
    print("Value at index 1:")
    print(l.get(1))
    l.update(1, 9)
    print("List after update:")
    l.print_list()
    l.sort()
    print("Sorted list:")
    l.print_list()
    l.reverse()
    print("Reversed list:")
    l.print_list()


# ----------------------------------------------------------------------
# 5. QUEUE
# ----------------------------------------------------------------------
class Queue:
    def __init__(self):
        self.data: TypingList[int] = []

    def enqueue(self, value: int):
        self.data.append(value)

    def dequeue(self):
        if self.is_empty():
            print("Queue is empty")
            return None
        return self.data.pop(0)

    def peek(self):
        if self.is_empty():
            print("Queue is empty")
            return None
        return self.data[0]

    def is_empty(self):
        return len(self.data) == 0

    def size(self):
        return len(self.data)

    def print_queue(self):
        print(self.data)


def demo_queue():
    print("\n--- Queue ---")
    q = Queue()
    for v in [5, 10, 3, 8]:
        q.enqueue(v)
    print("Queue:")
    q.print_queue()
    print("Dequeued value:")
    print(q.dequeue())
    print("Queue after dequeue:")
    q.print_queue()
    print("Front value:")
    print(q.peek())
    print("Is queue empty?")
    print(q.is_empty())
    print("Queue size:")
    print(q.size())


# ----------------------------------------------------------------------
# 6. SET
# ----------------------------------------------------------------------
class Set:
    def __init__(self):
        self.data: set[int] = set()

    def add(self, value: int):
        self.data.add(value)

    def remove(self, value: int):
        if value in self.data:
            self.data.remove(value)
        else:
            print("Value not found in set")

    def union(self, other_set: "Set") -> set[int]:
        return self.data.union(other_set.data)

    def intersection(self, other_set: "Set") -> set[int]:
        return self.data.intersection(other_set.data)

    def difference(self, other_set: "Set") -> set[int]:
        return self.data.difference(other_set.data)

    def is_subset(self, other_set: "Set") -> bool:
        return self.data.issubset(other_set.data)

    def is_superset(self, other_set: "Set") -> bool:
        return self.data.issuperset(other_set.data)

    def print_set(self):
        print(self.data)


def demo_set():
    print("\n--- Set ---")
    s1 = Set()
    for v in [1, 2, 3, 4]:
        s1.add(v)
    s2 = Set()
    for v in [3, 4, 5, 6]:
        s2.add(v)
    print("Set 1:")
    s1.print_set()
    print("Set 2:")
    s2.print_set()
    print("Union:")
    print(s1.union(s2))
    print("Intersection:")
    print(s1.intersection(s2))
    print("Difference:")
    print(s1.difference(s2))
    print("Is Set 1 a superset of Set 2?")
    print(s1.is_superset(s2))
    print("Is Set 2 a subset of Set 1?")
    print(s2.is_subset(s1))


# ----------------------------------------------------------------------
# 7. BINARY TREE (BST)
# ----------------------------------------------------------------------
class TreeNode:
    def __init__(self, value: int):
        self.value = value
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None


class BinaryTree:
    def __init__(self):
        self.root: Optional[TreeNode] = None

    def insert(self, value: int) -> None:
        if not self.root:
            self.root = TreeNode(value)
        else:
            self._insert(self.root, value)

    def _insert(self, node: TreeNode, value: int) -> None:
        if value < node.value:
            if node.left:
                self._insert(node.left, value)
            else:
                node.left = TreeNode(value)
        else:
            if node.right:
                self._insert(node.right, value)
            else:
                node.right = TreeNode(value)

    def inorder(self) -> None:
        self._inorder(self.root)
        print()

    def _inorder(self, node: Optional[TreeNode]) -> None:
        if node:
            self._inorder(node.left)
            print(node.value, end=" ")
            self._inorder(node.right)

    def preorder(self) -> None:
        self._preorder(self.root)
        print()

    def _preorder(self, node: Optional[TreeNode]) -> None:
        if node:
            print(node.value, end=" ")
            self._preorder(node.left)
            self._preorder(node.right)

    def postorder(self) -> None:
        self._postorder(self.root)
        print()

    def _postorder(self, node: Optional[TreeNode]) -> None:
        if node:
            self._postorder(node.left)
            self._postorder(node.right)
            print(node.value, end=" ")

    def search(self, value: int) -> bool:
        return self._search(self.root, value)

    def _search(self, node: Optional[TreeNode], value: int) -> bool:
        if not node:
            return False
        if value == node.value:
            return True
        elif value < node.value:
            return self._search(node.left, value)
        else:
            return self._search(node.right, value)


def demo_binary_tree():
    print("\n--- Binary Tree ---")
    bt = BinaryTree()
    for v in [5, 3, 7, 2, 4, 6, 8]:
        bt.insert(v)
    print("Inorder traversal:")
    bt.inorder()
    print("Preorder traversal:")
    bt.preorder()
    print("Postorder traversal:")
    bt.postorder()
    print("Is 6 in the tree?")
    print(bt.search(6))
    print("Is 9 in the tree?")
    print(bt.search(9))


# ----------------------------------------------------------------------
# 8. TUPLE
# ----------------------------------------------------------------------
class Tuple:
    def __init__(self, *args: object) -> None:
        self.data: tuple[object, ...] = args

    def get(self, index: int) -> object | None:
        if index < len(self.data):
            return self.data[index]
        else:
            print("Index out of range")
            return None

    def length(self):
        return len(self.data)

    def print_tuple(self):
        print(self.data)

    def index_of(self, value: object) -> int | None:
        try:
            return self.data.index(value)
        except ValueError:
            print("Value not found in tuple")

    def count(self, value: object) -> int:
        return self.data.count(value)


def demo_tuple():
    print("\n--- Tuple ---")
    t = Tuple(1, 2, 3, 4, 5, 2, 3)
    print("Tuple:")
    t.print_tuple()
    print("Value at index 2:")
    print(t.get(2))
    print("Length of tuple:")
    print(t.length())
    print("Index of value 3:")
    print(t.index_of(3))
    print("Count of value 2:")
    print(t.count(2))


# ----------------------------------------------------------------------
# MAIN - RUN ALL / MENU
# ----------------------------------------------------------------------
def run_all():
    demo_dictionary()
    demo_graph()
    demo_linked_list()
    demo_list()
    demo_queue()
    demo_set()
    demo_binary_tree()
    demo_tuple()


def main():
    demos = {
        "1": ("Dictionary", demo_dictionary),
        "2": ("Graph", demo_graph),
        "3": ("Linked List", demo_linked_list),
        "4": ("List", demo_list),
        "5": ("Queue", demo_queue),
        "6": ("Set", demo_set),
        "7": ("Binary Tree", demo_binary_tree),
        "8": ("Tuple", demo_tuple),
        "9": ("Run All", run_all),
    }
    while True:
        print("\n======== DATA STRUCTURES ========")
        for k, (name, _) in demos.items():
            print(f"{k}. {name}")
        print("0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Bye!")
            break
        if choice in demos:
            demos[choice][1]()
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()