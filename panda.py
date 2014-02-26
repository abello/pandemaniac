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
import random


SURROUNDING_NEIGHBORS = 2

# Load data from file given by command line argument
filename = sys.argv[1]
N = int(filename.split('.')[-3])
# i = int(sys.argv[2])
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
best1 = random.sample(sorted_centrality_nodes[:N], int(0.4 * N))
best2 = random.sample(sorted_centrality_nodes[N:N + N], int(0.3 * N))
best3 = random.sample(sorted_centrality_nodes[N + N:N + N + N], int(0.3 * N))

alll = best1 + best2 + best3

if len(alll) < N:
    for node in sorted_centrality_nodes[N + N + N:N + N + N + N]:
        alll.append(node)
        if len(alll) == N:
            break
for node in alll:
    print node


# d = nx.degree_centrality(G)
# sorted_centrality_nodes = sorted(d.keys(), key=lambda k: d[k], reverse=True)
# deg_centrality_nodes = sorted_centrality_nodes[:N]
# 
# graph = nx.to_dict_of_lists(G)
# nodes = {"par_closeness_centrality": par_closeness_centrality_nodes, "degree_centrality": deg_centrality_nodes}
# s = sim.run(graph, nodes)
# print s

