#!/usr/bin/python

import sys
import matplotlib.pyplot as plt
import networkx as nx
import json
import heapq as heap
from operator import itemgetter
import numpy as np
import sim
from multiprocessing import Pool, Manager, Lock


# Load data from file given by command line argument
filename = sys.argv[1]
N = int(filename.split('.')[-3])
f = open(filename)
graph_data = json.load(f)
f.close()

G = nx.from_dict_of_lists(graph_data)

def save_graph(graph, save_name):
    '''
    Saves networkx graph "graph" as pdf named "save_name"
    Source: http://stackoverflow.com/a/17388676
    '''

    #initialze Figure
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph,pos)
    nx.draw_networkx_edges(graph,pos)
    nx.draw_networkx_labels(graph,pos)

    cut = 1.00
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)

    plt.savefig(save_name, bbox_inches="tight")
    del fig

#Assuming that the graph g has nodes and edges entered
# save_graph(G, filename + '-visualization.pdf')

# Remove lone nodes
G.remove_nodes_from(nx.isolates(G))


# Degree centrality
# d = G.degree()
# sorted_deg_nodes = sorted(d.keys(), key=lambda k: d[k], reverse=True)
# high_degree_nodes = sorted_deg_nodes[:N]

# spaced_high_degree_nodes = []

# for node in sorted_deg_nodes:
#     is_a_neighbor = False

#     for gc in spaced_high_degree_nodes:
#         if node in G.neighbors(gc):
#             is_a_neighbor = True
#             break

#     if not is_a_neighbor:
#         spaced_high_degree_nodes.append(node)

#     if len(spaced_high_degree_nodes) == N:
#         break

# print "-" * 20
# print "spaced high degree nodes:"

# for choice in spaced_high_degree_nodes:
#     print choice

# for choice in spaced_high_degree_nodes:
#     print "degree: " + str(d[choice]) + ". node: " + choice


# print "-" * 20
# print "high degree nodes:"
# for node in high_degree_nodes:
#     print node
# for node in high_degree_nodes:
#     print "degree: " + str(d[node]) + ". node: " + node


# print "-" * 20
# print "strategies:"

# d = nx.load_centrality(G)
# sorted_centrality_nodes = sorted(d.keys(), key=lambda k: d[k], reverse=True)
# load_centrality_nodes = sorted_centrality_nodes[:N]

# d = nx.communicability_centrality(G)
# sorted_centrality_nodes = sorted(d.keys(), key=lambda k: d[k], reverse=True)
# comm_centrality_nodes = sorted_centrality_nodes[:N]

# for node in load_centrality_nodes:
#     print node

def load_c(n):
    val = nx.load_centrality(G, n)
    print "adding"
    d[n] = val

    
manager = Manager()
d = manager.dict()
l = Lock()
pool = Pool()

nodes = G.nodes()

pool.map(load_c, nodes)
pool.close()
pool.join()

print d


# graph = nx.to_dict_of_lists(G)
# nodes = {"load_centrality": sorted_centrality_nodes, "comm_centrality": comm_centrality_nodes}
# s = sim.run(graph, nodes)
# print s


#d = nx.betweenness_centrality(G)
#btwn = heap.nlargest(N, d, key = lambda k: d[k])
