import networkx as nx
import itertools
from girvannewman import _modularity
from girvannewman import girvannewman
from networkx.algorithms.community.quality import modularity
import matplotlib.pyplot as plt

def bis_communities(g, k):
    comp = nx.community.girvan_newman(g)
    limited = itertools.takewhile(lambda c: len(c) <= k, comp)
    for communities in limited:
        return (tuple(sorted(c) for c in communities))
    
def bis_modularity(g):
    best_Q = -100
    best_partition = None 

    g_current = g.copy()

    while g_current.number_of_edges() > 0:
        betweenness = nx.edge_betweenness_centrality(g_current)
        edge = max(betweenness, key=lambda e: betweenness[e])
        g_current.remove_edge(*edge)
        partition = list(nx.connected_components(g_current))
        Q = modularity(g, partition)

        if Q > best_Q :
            best_Q = Q
            best_partition = partition
    return best_partition, best_Q


def bis_dendogram(g):
    composition = nx.girvan_newman(g)

    partitions = []
    for partition in composition :
        partitions.append(partition)
    
    return partitions

