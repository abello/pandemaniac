#!/usr/bin/python

import sys
import matplotlib.pyplot as plt
import networkx as nx
import json
import heapq as heap


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
save_graph(G, filename + '-visualization.pdf')

with open('out.txt') as f:
    for (node, deg) in heap.nlargest(N, (G.degree_iter(),key=itemgetter(1),reverse=True)):
        f.write(str(node) + "\n")

    
    
