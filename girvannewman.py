from Graph import Graph
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt
from copy import deepcopy

"""
TODO list:
    - Compute betweeness
    - Remove highest betweeness edge
    - Check end condition

What I found as end conditions:
    - Modularity (a way to tell when a graph is modular enough)
    - Remove every edge and produce a full dendrogram
    - Max nb of communities reached
    others ?

What I found for betweeness:
    - Brandes Algorithm (ref: https://en.wikipedia.org/wiki/Brandes%27_algorithm, https://www.sciencedirect.com/science/article/pii/S0378873307000731?via%3Dihub)



What has been done:
    Brandes Algorithm v0.1
"""

def brandes(g: Graph):
    # computed betweeness
    CB = dict()

    # we loop over all graph vertices
    for s in g.vertices:
        # initialize delta, prev, sigma and dist values for current loop
        delta = {k:0 for k in g.vertices}
        prev = {k:[] for k in g.vertices}
        sig = {k:0 for k in g.vertices}
        dist = {k:float('inf') for k in g.vertices}

        # the source is set to a dist of 0 and sigma of 1
        sig[s] = 1
        dist[s] = 0

        # forward bfs

        queue = [s,]
        stack = []

        while len(queue) > 0:
            w = queue.pop(0)
            stack = [w,] + stack

            for v in g.get_neighborhood(w):
                if dist[v] == float('inf'):
                    dist[v] = dist[w] + 1
                    queue.append(v)
                if dist[v] == dist[w] + 1:
                    sig[v] = sig[v] + sig[w]
                    prev[v].append(w)

        # backpropagation

        while len(stack) > 0:
            w = stack.pop(0)
            for v in prev[w]:
                c = (sig[v]/sig[w]) * (1+delta[w])

                # ensure always same order (alphebetical)
                edge = '.'.join(list(sorted((v, w))))
                
                CB[edge] = CB.get(edge, 0) + c
                delta[v] += c

    return CB 


def modularity(g_original, partition):
    """Calculates the modularity of a graph
    Parameters : Graph"""

    m = g_original.nb_edges

    degrees = {}

    for vertex in g_original.vertices:
        degrees[vertex] = g_original.get_length_neighborhood(vertex)

    communitie_part ={}
    for index, community in enumerate(partition):
        for vertex in community :
            communitie_part[vertex] = index

    Q = 0

    for i in g_original.vertices:
        for j in g_original.vertices :
            if communitie_part[i] == communitie_part[j]:
                sij = 1
            else:
                sij = -1
            if j in g_original.get_neighborhood(i):
                A_ij = 1
            else :
                A_ij = 0
            calcul = (A_ij -(degrees[i] *degrees[j])/(2*m) *sij)
            Q+= calcul

    return Q/(4*m)
            
def bfs(g_current, source):
    distances = {}
    nb_paths = {}
    befores ={}

    for v in g_current.vertices:
        distances[v] = -1
        nb_paths[v] = 0
        befores[v] = []
    order_visited = []

    distances[source] = 0
    nb_paths[source] = 1

    file =[source]

    while file != [] :
        visited = file.pop(0)
        order_visited.append(visited)

        for v in g_current.get_neighborhood(visited):
            if distances[v] == -1:
                distances[v] = distances[visited] + 1
                file.append(v)

            if distances[v] == distances[visited] + 1:
                nb_paths[v] += nb_paths[visited]
                befores[v].append(visited)

    return distances, nb_paths, befores, order_visited 

def connexion(g):
    visited = set()
    partition= []
    composed = []
    for vertex in g.vertices : 
        if vertex not in visited : 
            distances, nb_paths, befores, order_visited = bfs(g, vertex)
            if distances[vertex] != -1 :
                composed.append(vertex)
            visited.update(composed)
            partition.append(composed)
    return partition 

def _modularity(g: Graph):
    best_Q = -100
    best_partition = None 

    while g.nb_edged > 0:
        betweenness = brandes(g)
        edge = max(betweenness, key=lambda e: betweenness[e])
        u, v = edge.split('.')
        g.remove_edge(u,v)
        partition = connexion(g)
        Q = modularity(g, partition)

        if Q > best_Q :
            best_Q = Q
            best_partition = partition
    return best_partition, best_Q

# g = Graph()
# g.add_vertex("A")
# g.add_vertex("B")
# g.add_vertex("C")
# g.add_vertex("D")
# g.add_edge("A", "B")
# g.add_edge("C", "D")

# # On teste modularity avec une bonne partition
# partition = [{"A","B"}, {"C","D"}]
# Q = modularity(g, partition)
# print(f"Q bonne partition : {Q}")


def _dendrogram(g: Graph):
    g_copy = deepcopy(g)

    edge_removal_order = []

    while g_copy.nb_edges > 0:
        betweenness = brandes(g_copy)

        max_betweeness = max(betweenness.items(), key = lambda x: x[1])[0]

        u,v = max_betweeness.split(".")

        edge_removal_order.append((u, v))

        g_copy.remove_edge(u, v)


    # the goal of the following operation is to build a linkage matrix for the dendrogram function
    linkage_matrix = []

    clusters = [{v} for v in g_copy.vertices]
    clusters_height = [1.0 for _ in g_copy.vertices]
    vertex_cluster_index = {v:i for i,v in enumerate(g_copy.vertices)}


    # for any further new clusters, the next index
    next_cluster_index = len(g_copy.vertices)


    for i, (u,v) in enumerate(edge_removal_order[::-1]):
        u_cluster = vertex_cluster_index[u]
        v_cluster = vertex_cluster_index[v]

        # If the clusters of u and v are different, then it must mean that they get joined by the current edge
        # If they are equal <=> u and v are in the same cluster and dont change the dendrogram (no separation of communities)
        if u_cluster != v_cluster:
            clusters.append(clusters[u_cluster]|clusters[v_cluster])
            clusters_height.append(clusters_height[u_cluster]+clusters_height[v_cluster])

            for j in clusters[-1]:
                vertex_cluster_index[j] = next_cluster_index
            next_cluster_index += 1

            linkage_matrix.append([
                u_cluster, # the 2 clusters that are merged
                v_cluster,
                clusters_height[-1], # the height of the merge
                len(clusters[-1])]  # the new size of the cluster merge
                )

    dendrogram(linkage_matrix, orientation="left", labels=g_copy.vertices)
    plt.show()




def _communities(g: Graph, k: int):
    pass


def girvannewman(g: Graph, method: str="modularity", k: int|None = None):
    match method:
        case "modularity":
            _modularity(g)
        case "dendrogram":
            _dendrogram(g)
        case "communities":
            _communities(g, k)
        case _:
            raise ValueError("Method is not valid, should be 'modularity', 'dendrogram' or 'communities'")


if __name__ == '__main__':
    # Butterfly graph :-)
    # g = Graph()
    # g.add_vertex("A")
    # g.add_vertex("B")
    # g.add_vertex("C")

    # g.add_edge("A", "B")
    # g.add_edge("A", "C")
    # g.add_edge("B", "C")

    # g.add_vertex("D")
    # g.add_vertex("E")
    # g.add_vertex("F")

    # g.add_edge("D", "E")
    # g.add_edge("D", "F")
    # g.add_edge("E", "F")

    # g.add_edge("C", "D")

    from loader import load_karate
    girvannewman(load_karate()[0], method="dendrogram")



    # print(list(set(("1", "2"))))
    # print(list(set(("2", "1"))))


    # for e,c in sorted(brandes(g).items(), key=lambda x: x[1]):
    #     print(f"{e} = {c}")

    # g.plot(labels=True)

    # from loader import load_karate

    # karate_graph, groups = load_karate()

    # for e,c in sorted(brandes(karate_graph).items(), key=lambda x: x[1]):
    #     print(f"{e} = {c}")

    # karate_graph.plot(labels=True)
