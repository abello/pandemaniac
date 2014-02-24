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

def calc_closeness(n):
    val = nx.closeness_centrality(G, n)
    l.acquire()
    d[n] = val
    l.release()


m = Manager()
d = m.dict()
l = Lock()
p = Pool()

nodes = G.nodes()
p.map(calc_closeness, nodes)
p.close()
p.join()



sorted_centrality_nodes = sorted(d.keys(), key=lambda k: d[k], reverse=True)
par_closeness_centrality_nodes = sorted_centrality_nodes[:N]

for node in par_closeness_centrality_nodes:
    print node

# graph = nx.to_dict_of_lists(G)
# nodes = {"par_closeness_centrality": par_closeness_centrality_nodes, "closeness_centrality": deg_centrality_nodes}
# s = sim.run(graph, nodes)
# print s
