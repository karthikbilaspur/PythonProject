import sys
import heapq

def dijkstra(graph: dict[str, dict[str, int]], start_node: str) -> dict[str, float]:
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0
    unvisited_nodes = [(0, start_node)]

    while unvisited_nodes:
        current_distance, current_node = heapq.heappop(unvisited_nodes)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(unvisited_nodes, (distance, neighbor))

    return distances

def shortest_path(graph: dict[str, dict[str, int]], start_node: str, end_node: str) -> tuple[list[str], float]:
    distances = dijkstra(graph, start_node)
    path = []
    current_node = end_node

    while current_node != start_node:
        path.append(current_node)
        for neighbor, weight in graph[current_node].items():
            if distances[current_node] - weight == distances[neighbor]:
                current_node = neighbor
                break

    path.append(start_node)
    path.reverse()

    return path, distances[end_node]

