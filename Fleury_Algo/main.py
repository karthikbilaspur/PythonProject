def is_valid_next_edge(graph, u, v):
    if graph[u][v] == 0:
        return False

    count = sum(1 for i in range(len(graph)) if graph[u][i] > 0)

    if count == 1:
        return True

    visited = [False] * len(graph)
    count1 = dfs_count(graph, u, visited)

    graph[u][v] -= 1
    graph[v][u] -= 1
    visited = [False] * len(graph)
    count2 = dfs_count(graph, u, visited)

    graph[u][v] += 1
    graph[v][u] += 1

    return count1 > count2


def dfs_count(graph, v, visited):
    count = 1
    visited[v] = True
    for i in range(len(graph)):
        if graph[v][i] > 0 and not visited[i]:
            count += dfs_count(graph, i, visited)
    return count


def fleury(graph):
    current_path = []
    current_vertex = 0
    num_edges = sum(sum(row) for row in graph) // 2

    for _ in range(num_edges):
        found = False
        for v in range(len(graph)):
            if graph[current_vertex][v] > 0 and is_valid_next_edge(graph, current_vertex, v):
                current_path.append((current_vertex, v))
                graph[current_vertex][v] -= 1
                graph[v][current_vertex] -= 1
                current_vertex = v
                found = True
                break

        if not found:
            break

    return current_path


