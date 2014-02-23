#!/usr/bin/python

import sys
import matplotlib.pyplot as plt
import networkx as nx
import json
import heapq as heap
from operator import itemgetter
import numpy as np


# Load data from file given by command line argument
filename = sys.argv[1]
N = int(sys.argv[2])
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
d = G.degree()
sorted_deg_nodes = heap.nlargest(N * 10, d, key = lambda k: d[k])

#threshold = np.percentile(d.values(), 70)

# TODO: Filter out nodes with degree less than threshold
good_choices = []
for node in sorted_deg_nodes:
    is_a_neighbor = False

    for gc in good_choices:
        if node in G.neighbors(gc):
            is_a_neighbor = True
            break

    if not is_a_neighbor:
        good_choices.append(node)

    if len(good_choices) == N:
        break

print good_choices





# TODO: Calculate load_centrality and communicability centrality

# TODO: Do all of that in parallel

# TODO: Run a simulation of all of them


#d = nx.betweenness_centrality(G)
#btwn = heap.nlargest(N, d, key = lambda k: d[k])

     

    
#with open('out.txt', 'w+') as f:
    
