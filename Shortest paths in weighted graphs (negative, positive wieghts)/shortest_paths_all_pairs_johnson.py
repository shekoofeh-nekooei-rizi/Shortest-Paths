# -*- coding: utf-8 -*-
"""shortest_paths_all_pairs_Johnson.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TXiN990_08cuaStD3Ix9Vh6lxN_1qsS0

# **Author: Shekoofhe Nekooei Rizi**


In this program, I implement the **Johnson's algorithm** to find the shortest paths between all pairs of vertices in a directed and weighted graph.

The edge weights might be positive or negative (or zero).


The vertices of the input graph are consecutive integers from 1 to n.

The edges are represented as a list of tuples in the form of (head, tail, weight), where weight is the cost of the directed edge from tail to head.

In this implementation if there is a negative cycle in the input, the program does not compute shortest paths/distances even for the parts of the graph where the negative cycle will not affect.


I provide small examples, followed by a sample using larger dataset to evaluate the program's performance.

In my experiment, this program took around 45 seconds to compute shortest distances and paths in "sample_3.txt" input.

"sample_3.txt" represents a graph with 1000 nodes and ~48000 edges.
"""

import numpy as np
import heapq
from collections import defaultdict

def johnson_all_pairs(n, edges):
    """ This function computes shortest paths between all pairs using Johnson's algorithm.

    Input:
    n: The number of nodes in the graph. Note that vertices are consecutive integers from 1 to n (inclusive).

    edges: A list of tuples in the form of (head, tail, weight), where weight is the cost of the directed edge from tail to head.


    Output:
    If there is a negative cycle in the input, the program prints: "There is a negative cycle in this input graph" and terminates.

    If there is no negative cycle, the output contains two matrices as follows:

    shortest_distances: numpy.ndarray(shape=(n, n))
    It stornes the shortest path distances between all pairs of nodes.
    shortest_distances[i][j] (or shortest_distances[i,j]) is the shortest path distance (lowest cost path) from node i+1 to j+1.

    shortest_paths: list of lists of edges in the form of (head, tail, weight).
    shortest_paths[i][j] is the shortest path (sequence of edges) from node i+1 to j+1.
    If there is no path, the element for the corresponding shortest path is [].
    """

    extra_edges = np.array([(0, v, 0) for v in range(1, n+1)])
    edges_2 = np.vstack([edges, extra_edges])

    infinity = np.inf
    d = np.full(n+1, infinity)
    d[0] = 0
    for _ in range(n):
        updated = False
        for u, v, w in edges_2:
            if d[v] > d[u] + w:
                d[v] = d[u] + w
                updated = True
        if not updated:
            break

    if updated:
        for u, v, w in edges_2:
            if d[v] > d[u] + w:
                print("There is a negative cycle in this input graph.")
                return None

    graph = defaultdict(list)
    revised_edges = [(u, v, w + d[u] - d[v]) for u, v, w in edges]
    for u, v, w in revised_edges:
        graph[u].append((v, w))

    shortest_distances = np.full((n+1, n+1), infinity)
    shortest_paths = [[[] for _ in range(n+1)] for _ in range(n+1)]

    for v in range(1, n+1):

        visited = np.zeros(n+1, dtype = bool)
        parent = {}
        H = []
        dist = np.full(n+1, infinity)
        dist[v] = 0
        heapq.heappush(H, (0, v))
        while H:
            l, current_node = heapq.heappop(H)
            if not visited[current_node]:
                visited[current_node] = True
                for neighbor, w in graph[current_node]:
                    if dist[neighbor] > l + w:
                        dist[neighbor] = l + w
                        heapq.heappush(H, (l + w, neighbor))
                        parent[neighbor] = (current_node, neighbor, w - d[current_node] + d[neighbor])


        for i in range(1, n+1):
            if dist[i] < infinity:
                shortest_distances[v, i] = dist[i] + d[i] - d[v]

            if i in parent:
                path = []
                node = i
                while node in parent:
                    path.append(parent[node])
                    node = parent[node][0]
                path.reverse()
                shortest_paths[v][i] = path
    shortest_paths = [row[1:] for row in shortest_paths[1:]]
    return shortest_distances[1:, 1:].view(), shortest_paths

"""## **Sample Tests**"""

n = 4
edges = [(1, 2, -10), (2, 3, 20), (3, 4, -30)]
johnson_all_pairs(n, edges)

n = 4
edges = [(1, 2, -10), (2, 1, -10), (3, 4, 20), (4, 3, 200)]
johnson_all_pairs(n, edges)

n = 3
edges = [(1, 2, 10), (2, 1, 10), (1, 3, 10), (3, 1, 10), (2, 3, 10), (3, 2, 10)]
johnson_all_pairs(n, edges)

"""### **Samples with Big Data**

The first line in the input file indicates the number of vertices and edges, respectively.

Each subsequent line describes a directed weighted edge:

the first two numbers are its tail and head, respectively, and the third number its length (cost).
"""

def read_input(file_name):
    with open(file_name, 'r') as file:
        n, m = map(int, file.readline().split())
        edges = np.loadtxt(file_name, skiprows = 1, dtype = int)
    return n, edges

def write_output_file(result_d, result_p, output_file_name):
    with open(output_file_name, 'w') as file:
        for d in result_d:
            file.write(str(d) + "\n")
        for p in result_p:
            if p is not None:
                file.write(str(p) + "\n")

n3, edges3 = read_input('sample_3.txt')

distances, paths = johnson_all_pairs(n3, edges3)

"""If we were to write the output of the above line to a file, it would be an enormous file, making it time-consuming to download or open.

Instead, I run some experiments with the results in a more manageable way:

I identify the shortest shortest path by finding all paths with the minimum distance.

I also determine the longest shortest paths.
"""

shortest_shortest_distance = distances.min()
min_locations = np.where(distances == shortest_shortest_distance)
print(min_locations)

print("The distance of the shortest shortest path is: ", distances[398, 903])
print("\nThe path is as follows from  399  to  904:")
paths[398][903]

longsest_shortest_distance = distances.max()
max_locations = np.where(distances == longsest_shortest_distance)
print(max_locations)

print("The distance of a longest shortest path is: ", distances[831, 1])
print("\nThis longets shortest path from  832   to  2  is as follows:")
paths[831][1]

print("The distance of the longest shortest path is: ", distances[831, 195])
print("\nThis longets shortest path from  832   to  196   is as follows:")
paths[831][195]

print("The distance of the longest shortest path is: ", distances[831, 197])
print("\nTThis longets shortest path from  832   to  198   is as follows:")
paths[831][197]

print("The distance of the longest shortest path is: ", distances[831, 398])
print("\nThis longets shortest path from  832   to  399   is as follows:")
paths[831][398]

print("The distance of the longest shortest path is: ", distances[831, 460])
print("\nThis longets shortest path from  832   to  461   is as follows:")
paths[831][460]

print("The distance of the longest shortest path is: ", distances[831, 527])
print("\nThis longets shortest path from  832   to  528  is as follows:")
paths[831][527]

start = int(input("Enter an integer between 1 to 1000 as your desired start node: "))
destination = int(input("Enter an integer between 1 to 1000 as your desired destination node:  "))

print("The shortest distance from node ", start, " to node ", destination, " is", distances[start-1, destination-1])
print("The shortest path between these two nodes is as follows:")
paths[start-1][destination-1]