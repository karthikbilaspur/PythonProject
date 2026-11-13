# Data Structures in Python — All in One File

All 8 classic data structures in one single file: data_structures.py
No HTML, no CSS, no JS. Just pure Python.

Structures Included
 Structure Class Key Operations

1 Dictionary Dictionary add, get, update, delete, sort by keys / values
2 Graph Graph add_node, add_edge, DFS, BFS
3 Linked List LinkedList append, print, sort
4 List List append, insert, delete, get, update, sort, reverse
5 Queue Queue enqueue, dequeue, peek, is_empty, size
6 Set Set add, remove, union, intersection, difference, subset / superset
7 Binary Tree (BST) BinaryTree insert, inorder, preorder, postorder, search
8 Tuple Tuple get, length, index_of, count

How to Run
python index.py
You will see a menu:

======== DATA STRUCTURES ========

1. Dictionary
2. Graph
3. Linked List
4. List
5. Queue
6. Set
7. Binary Tree
8. Tuple
9. Run All
0.Exit
Type a number and press Enter.
9 runs every demo back-to-back. 0 exits.

Use It in Your Own Code
You can also import any class directly — no need to run the menu:

from data_structures import Dictionary, Graph, Queue, BinaryTree

Dictionary

d = Dictionary()
d.add("apple", 5)
d.add("banana", 10)
print(d.get("apple"))        # 5
print(d.sort_by_values())    # {'apple': 5, 'banana': 10}

Queue (FIFO)
q = Queue()
q.enqueue(5)
q.enqueue(10)
print(q.dequeue())           # 5
print(q.peek())              # 10

Graph
g = Graph()
for n in ["A", "B", "C"]:
    g.add_node(n)
g.add_edge("A", "B")
g.add_edge("A", "C")
g.dfs("A")                   # A B C
g.bfs("A")                   # A B C

Binary Tree
bt = BinaryTree()
for v in [5, 3, 7, 2, 4]:
    bt.insert(v)
bt.inorder()                 # 2 3 4 5 7
print(bt.search(7))          # True
Example Output
--- Dictionary ---
Dictionary:
apple: 5
banana: 10
cherry: 3
date: 8

--- Graph ---
Graph:
A -> ['B', 'C']
B -> ['A', 'D']
DFS Traversal:
A B D E C

--- Linked List ---
Linked List:
64 34 25 12 22 11 90
Sorted Linked List:
11 12 22 25 34 64 90
Notes
List and Tuple are custom classes in this file, not typing.List / typing.Tuple. Inside the file, typing is imported as TypingList to avoid clashing.
The tree node is called TreeNode so it doesn't clash with the linked-list Node.
Tuple is immutable by design — there is no add / update / delete, only get, length, index_of, and count.
Graph is undirected: add_edge("A", "B") links both ways.
Queue.dequeue() on an empty queue prints "Queue is empty" and returns None.
File Structure
.
├── index.py   # Everything — all 8 classes + demos + menu
└── README.md            # This file
