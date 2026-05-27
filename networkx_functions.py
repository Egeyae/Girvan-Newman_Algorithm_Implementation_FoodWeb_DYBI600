import networkx as nx
import itertools
from girvannewman import _modularity
from girvannewman import _communities
from girvannewman import girvannewman
from networkx.algorithms.community.quality import modularity
import matplotlib.pyplot as plt
from Graph import Graph

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

def to_networkx(g):
    g_nx = nx.Graph()
    for v in g.vertices:
        g_nx.add_node(v)
    for v in g.vertices:
        for u in g.get_neighborhood(v):
            g_nx.add_edge(v, u)
    return g_nx


def comparison_communities(g, k):
    g_nx = to_networkx(g)
    ntx_partition = bis_communities(g_nx, k)
    best_partition_com = _communities(g,k, return_graph= False)

    in_communities = {}

    for i, community in enumerate(best_partition_com):
        for vertex in community:
            in_communities[str(vertex)] = i
    
    in_communities_ntx = {}

    for i, community in enumerate(ntx_partition):
        for vertex in community:
            in_communities_ntx[str(vertex)] = i

    resemblance = 0
    differences = 0
    total = len(in_communities)

    for vertex in in_communities:
        com_mod = {v for v in in_communities if in_communities[v] == in_communities[vertex]}
        com_nx = {v for v in in_communities_ntx if in_communities_ntx[v] == in_communities_ntx[vertex]}

        if com_mod == com_nx :
            resemblance +=1
        else:
            differences +=1
    
    total_resemblance = (resemblance/ total)*100

    return total_resemblance, resemblance, differences


def comparison_modularit(g):
    g_nx = to_networkx(g)
    ntx_partition, ntx_Q = bis_modularity(g_nx)
    best_partition_mod, best_Q_mod = _modularity(g, return_graph= False)

    in_communities = {}

    for i, community in enumerate(best_partition_mod):
        for vertex in community:
            in_communities[str(vertex)] = i
    
    in_communities_ntx = {}

    for i, community in enumerate(ntx_partition):
        for vertex in community:
            in_communities_ntx[str(vertex)] = i

    resemblance = 0
    differences = 0
    total = len(in_communities)

    for vertex in in_communities:
        com_mod = {v for v in in_communities if in_communities[v] == in_communities[vertex]}
        com_nx = {v for v in in_communities_ntx if in_communities_ntx[v] == in_communities_ntx[vertex]}

        if com_mod == com_nx :
            resemblance +=1
        else:
            differences +=1
    
    total_resemblance = (resemblance/ total)*100

    return total_resemblance, resemblance, differences

#test com 
from loader import load_karate
g, groups = load_karate()

print(comparison_modularit(g))


def bis_dendogram(g):
    composition = nx.girvan_newman(g)

    partitions = []
    for partition in composition :
        partitions.append(partition)
    
    return partitions

