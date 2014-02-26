#!/usr/bin/python

import sys
import matplotlib.pyplot as plt
import networkx as nx
import json
import heapq as heap
from operator import itemgetter
import numpy as np
import sim
import betweenness_centrality
from multiprocessing import Pool, Manager, Lock


SURROUNDING_NEIGHBORS = 2

# Load data from file given by command line argument
filename = sys.argv[1]
N = int(filename.split('.')[-3])
f = open(filename)
graph_data = json.load(f)
f.close()

G = nx.from_dict_of_lists(graph_data)

# Remove lone nodes
G.remove_nodes_from(nx.isolates(G))


# d = nx.closeness_centrality(G)
# sorted_centrality_nodes = sorted(d.keys(), key=lambda k: d[k], reverse=True)
# deg_centrality_nodes = sorted_centrality_nodes[:N]





# Parallelized closeness centrality calculations

def calc_closeness(n):
    val = nx.closeness_centrality(G, n)
    l.acquire()
    d[n] = val
    l.release()


m = Manager()
d = m.dict()   # Centrality dictionary
l = Lock()
p = Pool()

all_nodes = G.nodes()

p.map(calc_closeness, all_nodes)
p.close()
p.join()



sorted_centrality_nodes = sorted(d.keys(), key=lambda k: d[k], reverse=True)
par_closeness_centrality_nodes = sorted_centrality_nodes[:N]


def best_n_neighbors(nodes, n):
    good_nodes = []
    for node in nodes:
        best_neighbors = sorted(G.neighbors(node), key=lambda k:d[k], reverse=True)
        num_added = 0
        for neighbor in best_neighbors:
            if num_added == n:
                break
            if neighbor not in good_nodes:
                good_nodes.append(neighbor)
                num_added += 1
    return good_nodes



num_nodes_to_surround = N / SURROUNDING_NEIGHBORS
final_list = best_n_neighbors(par_closeness_centrality_nodes[:num_nodes_to_surround], SURROUNDING_NEIGHBORS)
if num_nodes_to_surround * SURROUNDING_NEIGHBORS != N:
    for node in sorted_centrality_nodes[num_nodes_to_surround:]:
        if node not in final_list:
            final_list.append(node)
            break

for node in final_list:
    print node

# d = nx.degree_centrality(G)
# sorted_centrality_nodes = sorted(d.keys(), key=lambda k: d[k], reverse=True)
# deg_centrality_nodes = sorted_centrality_nodes[:N]
# 
# graph = nx.to_dict_of_lists(G)
# nodes = {"par_closeness_centrality": par_closeness_centrality_nodes, "degree_centrality": deg_centrality_nodes}
# s = sim.run(graph, nodes)
# print s
