# -*- coding: utf-8 -*-
"""shortest_paths_all_pairs_Floyd-Warshall.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_EOhLAwlESbuUSp-ASdMJVBDYUpVqAYn

# **Author: Shekoofhe Nekooei Rizi**


In this program, I implement the **Floyd-Warshall algorithm** to find the shortest paths between all pairs of vertices in a directed and weighted graph.

The edge weights might be positive or negative (or possibly zero).

The vertices of the input graph are consecutive integers from 1 to n.

The edges are represented as a list of tuples in the form of (head, tail, weight), where weight is the cost of the directed edge from tail to head.

I provide small examples, followed by a sample using larger dataset to evaluate the program's performance.

All the samples in here are the same as the ones in the "shortest_paths_all_pairs_Bellman-Ford.py" program so that we could compare these two algorithms and implementation performance.

In my experiment, this implementation took around 5-6 minutes to compute the shortest paths in the "sample_3.txt" input.

"sample_3.txt" represents a graph with 1000 nodes and ~48000 edges.
"""

import numpy as np

def floyd_warshall(n, edges):
    """
    This function computes shortest paths between all pairs using Floyd-Warshall algorithm.

    Input:
    n: The number of nodes in the graph. Note that vertices are consecutive integers from 1 to n (inclusive).

    edges: A list of tuples in the form of (head, tail, weight), where weight is the cost of the directed edge from tail to head.

    Output:
    dist_matrix: np.ndarray(shape=(n, n))
    It stornes the shortest path distances between all pairs of nodes.
    dist_matrix[i][j] is the shortest path distance (lowest cost path) from node i+1 to j+1.
    If there is no path, or the path affected by a negative cycle the value for the corresponding shortest distance is inf or -inf, respectivly.

    path_matrix: list of lists of edges in the form of (head, tail, weight).
    path_matrix[i][j] is the shortest path from node i+1 to j+1.
    If there is no path, or the path affected by a negative cycle the value for the corresponding shortest path is None.
    """
    infinity = float('inf')

    dist = np.full((n, n), infinity)
    np.fill_diagonal(dist, 0)

    #path = np.full((n, n), None, dtype=object)
    path = [[None] * n for _ in range(n)]

    for u, v, w in edges:
        dist[u-1, v-1] = w
        #path[u-1, v-1] = [(u, v, w)]
        path[u-1][v-1] = [(u, v, w)]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i, j] > dist[i, k] + dist[k, j]:
                    dist[i, j] = dist[i, k] + dist[k, j]
                    if path[i][k] is not None and path[k][j] is not None:
                        path[i][j] = path[i][k] + path[k][j]


    negative_cycle_affected_nodes = set()

    for i in range(n):
        if dist[i, i] < 0:
            negative_cycle_affected_nodes.add(i)


    for k in negative_cycle_affected_nodes:
        for i in range(n):
            for j in range(n):
                if dist[i, k] < infinity and dist[k, j] < infinity:
                    dist[i, j] = -infinity
                    path[i][j] = None

    return dist, path

"""## **Sample Tests**"""

n = 4
edges = [(1, 2, -10), (2, 3, 20), (3, 4, -30)]
floyd_warshall(n, edges)

n = 4
edges = [(1, 2, -10), (2, 1, -10), (3, 4, 20), (4, 3, 200)]
floyd_warshall(n, edges)

n = 3
edges = [(1, 2, 10), (2, 1, 10), (1, 3, 10), (3, 1, 10), (2, 3, 10), (3, 2, 10)]
floyd_warshall(n, edges)

"""### **Samples with Big Data**

The first line in the input file indicates the number of vertices and edges, respectively.

Each subsequent line describes a directed weighted edge:

the first two numbers are its tail and head, respectively, and the third number its length (or weight or cost, whichever you would like to call).
"""

def read_input(filename):
    with open(filename, 'r') as file:
        first_line = file.readline().strip()
        n, m = map(int, first_line.split())
        edges = []
        for _ in range(m):
            line = file.readline().strip()
            u, v, w = map(int, line.split())
            edges.append([u, v, w])
    return n, edges

n3, edges3 = read_input('sample_3.txt')

distances, paths = floyd_warshall(n3, edges3)

"""Here, I run some experiments with the results in a manageable way since writing the results in a file would make an enormous-sized file.

I identify the shortest shortest path by finding all paths with the minimum distance.

I also determine the longest shortest paths.
"""

shortest_shortest_distance = distances.min()
min_locations = np.where(distances == shortest_shortest_distance)
print(min_locations)

shortest_shortest_path_dist = distances.min()
min_locations = np.where(distances == shortest_shortest_path_dist)
print("index positions for the shortest shortest paths: ", min_locations)

(u_s, v_s) = np.unravel_index(np.argmin(distances), distances.shape)
print(u_s + 1, "--->", v_s + 1, " is the shortest path among all shortest paths in sample_3.txt input.\n")
print("The total distance [cost] of this path is: ", shortest_shortest_path_dist)
print("\nThe sequence of edges in this path is as follows:")
paths[u_s][v_s]

longest_shortest_path_dist = distances.max()
max_locations = np.where(distances == longest_shortest_path_dist)
print("index positions for the longest shortest paths: ", max_locations)

print("The distance of the longest shortest path is: ", distances[831, 1])
print("\nOne of such paths is as follows: ", 832, "-->", 2)
paths[831][1]

print("The distance of the longest shortest path is: ", distances[831, 195])
print("\nOne of such paths is as follows: ", 832, "-->", 196)
paths[831][195]

print("The distance of the longest shortest path is: ", distances[831, 197])
print("\nOne of such paths is as follows: ", 832, "-->", 198)
paths[831][197]

print("The distance of the longest shortest path is: ", distances[831, 398])
print("\nOne of such paths is as follows: ", 832, "-->", 399)
paths[831][398]

print("The distance of the longest shortest path is: ", distances[831, 460])
print("\nOne of such paths is as follows: ", 832, "-->", 461)
paths[831][460]

print("The distance of the longest shortest path is: ", distances[831, 527])
print("\nOne of such paths is as follows: ", 832, "-->", 528)
paths[831][527]

start = int(input("Enter an integer between 1 to 1000 as your desired start node: "))
destination = int(input("Enter an integer between 1 to 1000 as your desired destination node:  "))

print("The shortest distance from node ", start, " to node ", destination, " is", distances[start-1, destination-1])
print("The shortest path between these two nodes is as follows:")
paths[start-1][destination-1]