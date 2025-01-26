# -*- coding: utf-8 -*-
"""shortest_paths_in_graph_between_all_pairs.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mg0YGM5x2LO8XbYNiSwD7R2cqscOoKF5

**Author: Shekoofeh Nekooei Rizi**

This program computes the shortest paths and corresponding lengths between all pairs of vertices in an unweighted/undirected given graph.

I implement Breadth First Search for this purpose.
"""

from collections import deque

def shortest_paths_all_pairs(n, edges):
    """
    This function computes the shortest paths and distances between all vertices in a given unweighted/undirected graph.

    The vertices of the given graph are consecutive integer numbers from 0 to "n" [inclusive].
    The "edges" is a list of undirected edges in the form of [u, v] showing an edge between two vertices u and v.

    The output is a dictionary with keys in the form of (start vertex, destination vertex) pairs, and values are in the form of (shortes distance, [shortest path])

    When there is no path between start vertex and destination vertex, shortest distance is 'inf' and the path is 'None'

    """
    graph = {v:[] for v in range(n+1)}
    for e in edges:
        graph[e[0]].append(e[1])
        graph[e[1]].append(e[0])

    infinity = float('inf')
    def bfs(source):
        nonlocal infinity
        dist = [infinity] * (n+1)
        dist[source] = 0

        visited = set()
        visited.add(source)

        Q = deque()
        Q.append(source)

        paths = {v: None for v in range(n+1)}
        paths[source] = [source]

        while Q:
            current_node = Q.popleft()
            for neighbor in graph[current_node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    dist[neighbor] = dist[current_node] + 1
                    paths[neighbor] = paths[current_node] + [neighbor]
                    Q.append(neighbor)

        return {(min(source, v), max(source, v)): (dist[v], paths[v]) for v in range(n+1) if v != source}

    all_pairs_shortest_paths = {}
    for start_vertex in range(n+1):
        all_pairs_shortest_paths.update(bfs(start_vertex))

    return all_pairs_shortest_paths

"""## **Small Samples**"""

n = 3
edges = [[0, 1], [1, 2], [2, 3]]
shortest_paths_all_pairs(n, edges)

n = 5
edges = [[0,1], [2, 1], [3, 1], [4, 1], [5, 1], [0, 2], [2, 3]]
shortest_paths_all_pairs(n, edges)

n = 10
edges = [[0,1], [1,2], [2,3], [3,4], [4,5], [0,6], [6,7], [7,8], [8,9], [9,10], [10,0]]
shortest_paths_all_pairs(n, edges)