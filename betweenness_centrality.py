## NOTE: Got thsi from
# https://networkx.lanl.gov/trac/attachment/ticket/594/betweenness_centrality.py
"""
Example of parallel implementation of betweenness centrality using the
multiprocessing module from Python Standard Library.

The function betweenness centrality accepts a bunch of nodes and computes 
the contribution of those nodes to the betweenness centrality of the whole 
network. Here we divide the network in chuncks of nodes and we compute their
contribution to the betweenness centrality of the whole network.
"""

from multiprocessing import Pool
import time
import itertools
import networkx as nx

def chunks(l,n):
    """Divide a list of nodes `l` in `n` chunks"""
    l_c = iter(l)
    while 1:
        x = tuple(itertools.islice(l_c,n))
        if not x:
            return
        yield x

def _betreduce(bt1,bt2):
    """Sum betweenness values of two dictionaries with nodes as keys"""
    for n in bt1:
        bt1[n] += bt2[n]
    return bt1

def _betmap((G,normalized,weight,sources)):
    """Pool for multiprocess only accepts functions with one argument. This function
    uses a tuple as its only argument.
    """
    return nx.betweenness_centrality_source(G,normalized,weight,sources)

def betweenness_centrality_parallel(G,processes=None):
    """Parallel betweenness centrality  function"""
    p = Pool(processes=processes)
    node_divisor = len(p._pool)*4
    node_chunks = list(chunks(G.nodes(),G.order()/node_divisor))
    num_chunks = len(node_chunks)
    bt_sc = p.map(_betmap,
                  zip([G]*num_chunks,
                      [True]*num_chunks,
                      [None]*num_chunks,
                      node_chunks))
    bt_c = reduce(_betreduce,bt_sc) 
    return bt_c

if __name__ == "__main__":
    G_ba = nx.barabasi_albert_graph(1000,3)
    G_er = nx.gnp_random_graph(1000,0.01)
    G_ws = nx.connected_watts_strogatz_graph(1000,4,0.1)
    for G in [G_ba, G_er, G_ws]:
        print
        print("Computing betweenness centrality for:")
        print(nx.info(G))
        print("Parallel version")
        start = time.time() 
        bt = betweenness_centrality_parallel(G)
        print("Time parallel version: %.4F"%(time.time()-start))
        print("Betweenness centrality for node 0: %.5f"%(bt[0]))
        print("Non-Parallel version")
        start = time.time() 
        bt = nx.betweenness_centrality(G)
        print("Time non-parallel version: %.4F"%(time.time()-start))
        print("Betweenness centrality for node 0: %.5f"%(bt[0]))
    print
