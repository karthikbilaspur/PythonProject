class Graph:
    def __init__(self):
        self.data = {}

    def add_node(self, node):
        if node not in self.data:
            self.data[node] = []

    def add_edge(self, node1, node2):
        if node1 in self.data and node2 in self.data:
            self.data[node1].append(node2)
            self.data[node2].append(node1)

    def print_graph(self):
        for node in self.data:
            print(node, "->", self.data[node])

    def dfs(self, start_node):
        visited = set()
        self._dfs_helper(start_node, visited)

    def _dfs_helper(self, node, visited):
        visited.add(node)
        print(node, end=" ")
        for neighbor in self.data[node]:
            if neighbor not in visited:
                self._dfs_helper(neighbor, visited)

    def bfs(self, start_node):
        visited = set()
        queue = [start_node]
        visited.add(start_node)
        while queue:
            node = queue.pop(0)
            print(node, end=" ")
            for neighbor in self.data[node]:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)

# Create a graph
g = Graph()
g.add_node("A")
g.add_node("B")
g.add_node("C")
g.add_node("D")
g.add_node("E")

g.add_edge("A", "B")
g.add_edge("A", "C")
g.add_edge("B", "D")
g.add_edge("C", "E")
g.add_edge("D", "E")

# Print the graph
print("Graph:")
g.print_graph()

# Perform DFS
print("\nDFS Traversal:")
g.dfs("A")

# Perform BFS
print("\n\nBFS Traversal:")
g.bfs("A")