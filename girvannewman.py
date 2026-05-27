from Graph import Graph
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt
from copy import deepcopy


LABEL_COLORS = [
    '#1f77b4',  # Blue
    '#ff7f0e',  # Orange
    '#2ca02c',  # Green
    '#d62728',  # Red
    '#9467bd',  # Purple
    '#8c564b',  # Brown
    '#e377c2',  # Pink
    '#7f7f7f',  # Gray
]

from collections import deque
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
            calcul = (A_ij -(degrees[i] *degrees[j])/(2*m)) *sij
            Q+= calcul

    return Q/(4*m)
            
def bfs_distances(g_current, source):
    distances = {v: -1 for v in g_current.vertices}
    distances[source] = 0

    file = deque([source])

    while len(file) > 0 :
        visited = file.popleft()
        for v in g_current.get_neighborhood(visited):
            if distances[v] == -1:
                distances[v] = distances[visited] + 1
                file.append(v) 
    return distances

def connexion(g):
    visited = set()
    partition= []
    for vertex in g.vertices : 
        composed = []
        if vertex not in visited : 
            distances = bfs_distances(g, vertex)
            composed = {v for v in g.vertices if distances[v] != -1}
            visited.update(composed)
            partition.append(composed)
    return partition 

def _modularity(g: Graph, return_graph: bool = False):
    best_Q = -100
    best_partition = None 
    modularity_list = []

    g_current = Graph()
    for v in g.vertices:
        g_current.add_vertex(v)
    for i in g.vertices:
        for v in g.get_neighborhood(i):
            if v not in g_current.get_neighborhood(i):
                g_current.add_edge(i,v)

    betweenness = brandes(g_current)

    while g_current.nb_edges > 0:
        edge = max(betweenness, key=lambda e: betweenness[e])
        u, v = edge.split('.')
        partition_before = connexion(g_current)

        before_com = None
        for community in partition_before:
            if u in community: 
                before_com = community
                break
            

        if v in g_current.get_neighborhood(u):
            g_current.remove_edge(u, v)
        elif u in g_current.get_neighborhood(v):
            g_current.remove_edge(v, u)
        else:
            break
        
        betweenness.pop(edge, None)

        partition_after = connexion(g_current)

        new_edges = []
        for community in partition_after:
            if community <= before_com:
                new_edges.append(community)
        
        for edges in new_edges:

            g_sub = Graph()
            for vertex in edges:
                g_sub.add_vertex(vertex)

            edges_sub = set()
            for vertex in edges :
                for neighbor in g_current.get_neighborhood(vertex):
                    g_sub.add_edge(vertex, neighbor)
                    edges_sub.add((vertex, neighbor))
            
            sub_betweenness = brandes(g_sub)
            for key, val in sub_betweenness.items():
                betweenness[key] = val
        
        partition_after = connexion(g_current)

        Q = modularity(g, partition_after)
        modularity_list.append(Q)

        if Q > best_Q :
            best_Q = Q
            best_partition = partition_after

    if not return_graph:
        return best_partition, best_Q
    else:
        return best_partition, best_Q, g_current


def _dendrogram(
    g: Graph,
    height_method: str | None = None,
    communities: list | None = None,
    colors: list = LABEL_COLORS,
    ax=None,
    title: str | None = None
):
    assert height_method in (None, "modularity")

    # make a copy of g, so we can make all modifications we want
    g_copy = deepcopy(g)
    edge_removal_order = []

    # apply girvan-newman up until no edges remain
    while g_copy.nb_edges > 0:
        betweenness = brandes(g_copy)
        max_betweeness = max(betweenness.items(), key=lambda x: x[1])[0]
        u, v = max_betweeness.split(".")
        edge_removal_order.append((u, v))
        g_copy.remove_edge(u, v)

    # Build linkage matrix
    linkage_matrix = []
    clusters = [{v} for v in g_copy.vertices]
    clusters_height = [1.0 if height_method is None else 0.0 for _ in g_copy.vertices]
    vertex_cluster_index = {v: i for i, v in enumerate(g_copy.vertices)}
    next_cluster_index = len(g_copy.vertices)

    for i, (u, v) in enumerate(edge_removal_order[::-1]):
        u_cluster = vertex_cluster_index[u]
        v_cluster = vertex_cluster_index[v]
        g_copy.add_edge(u, v)

        if u_cluster != v_cluster:
            clusters.append(clusters[u_cluster] | clusters[v_cluster])

            if height_method is None:
                clusters_height.append(clusters_height[u_cluster] + clusters_height[v_cluster])
            elif height_method == "modularity":
                partition = dict()
                for v, j in vertex_cluster_index.items():
                    if j not in partition.keys():
                        partition[j] = []
                    partition[j].append(v)
                clusters_height.append(1 - modularity(g_copy, list(partition.values())))

            for j in clusters[-1]:
                vertex_cluster_index[j] = next_cluster_index
            next_cluster_index += 1

            linkage_matrix.append([
                u_cluster,
                v_cluster,
                clusters_height[-1],
                len(clusters[-1])
            ])

    user_ax = ax is not None
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))

    ax.cla()  # Clear the axis

    # Plot dendrogram ON THE PROVIDED AXIS
    dendrogram(
        linkage_matrix,
        orientation="left",
        labels=g_copy.vertices,
        ax=ax  # This is critical
    )

    if communities is not None:
        vertex_to_color = {}
        for i, community in enumerate(communities):
            for vertex in community:
                vertex_to_color[str(vertex)] = colors[i % len(colors)]
        for lbl in ax.get_yticklabels():
            lbl.set_color(vertex_to_color[lbl.get_text()])

    if title:
        ax.set_title(title)

    if not user_ax:
        plt.tight_layout()
        plt.show()

    return ax


def _communities(g: Graph, k: int, return_graph: bool = False):
    g_copy = deepcopy(g)

    while g_copy.nb_edges != 0:
        betweenness = brandes(g_copy)

        edge = max(betweenness, key=lambda e: betweenness[e])
        u, v = edge.split('.')

        if v in g_copy.get_neighborhood(u):
            g_copy.remove_edge(u, v)
        elif u in g_copy.get_neighborhood(v):
            g_copy.remove_edge(v, u)
        
        partition = connexion(g_copy)

        if len(partition) >= k :
            if not return_graph:
                return partition
            else:
                return partition, g_copy

    if not return_graph:
        return partition
    else:
        return partition, g_copy


def girvannewman(g: Graph, method: str="modularity", 
    k: int|None = None, 
    height_method: str|None = None, 
    return_graph: bool = False, 
    communities: list|None = None, 
    label_colors: list = LABEL_COLORS,
    title: str|None = None,
    ax = None):
    match method:
        case "modularity":
            return _modularity(g, return_graph= return_graph)
        case "dendrogram":
            _dendrogram(g, height_method=height_method, communities=communities, colors = label_colors, title=title, ax=ax)
        case "communities":
            return _communities(g, k, return_graph=return_graph)
        case _:
            raise ValueError("Method is not valid, should be 'modularity', 'dendrogram' or 'communities'")


if __name__ == '__main__':
    # Butterfly graph :-)
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_vertex("C")

    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "C")

    g.add_vertex("D")
    g.add_vertex("E")
    g.add_vertex("F")

    g.add_edge("D", "E")
    g.add_edge("D", "F")
    g.add_edge("E", "F")

    g.add_edge("C", "D")

    from loader import load_karate
    girvannewman(load_karate()[0], method="dendrogram")
    karate_graph = load_karate()[0]
    partition = girvannewman(karate_graph, method="communities", k=5)

    print(f"Numebr of communities : {len(partition)}")
    for i, community in enumerate(partition):
        print(f"Community {i} : {community}")

    colors = {}
    color_list = ["red", "blue", "green", "yellow", "purple", "orange"]
    for i, community in enumerate(partition):
        for vertex in community:
            colors[vertex] = color_list[i % len(color_list)]

    karate_graph.plot(
        labels=True,
        colors=[colors[v] for v in karate_graph.vertices]
    )



    print(list(set(("1", "2"))))
    print(list(set(("2", "1"))))


    for e,c in sorted(brandes(g).items(), key=lambda x: x[1]):
      print(f"{e} = {c}")

    g.plot(labels=True)

    from loader import load_karate

    karate_graph, groups = load_karate()

    for e,c in sorted(brandes(karate_graph).items(), key=lambda x: x[1]):
        print(f"{e} = {c}")

    karate_graph.plot(labels=True)
    karate_graph.plot(labels=True)

#test
#best_partition, best_Q, Q_values = _modularity(karate_graph)
#print(best_partition)

#fig, ax = plt.subplots()
#ax.plot(Q_values)
#ax.set_xlabel("edges erased")
#ax.set_ylabel("Q")
#ax.set_title("Evolution of modularity ")
#ax.axhline(y=best_Q, color='red', linestyle='--', label=f"Meilleur Q = {best_Q:.3f}")
#ax.legend()
#plt.show()

#colors = {}
#color_list = ["red", "blue", "green", "yellow", "purple", "orange"]
#for i, community in enumerate(best_partition):
    #for vertex in community:
        #colors[vertex] = color_list[i % len(color_list)]

#karate_graph.plot(
    #labels=True,
    #colors=[colors[v] for v in karate_graph.vertices]
#)


    from loader import load_karate
    girvannewman(load_karate()[0], method="modularity", return_graph= False)
    karate_graph = load_karate()[0]
    partition = girvannewman(karate_graph, method="modularity", k=5)

    print(f"Numebr of communities : {len(partition)}")
    for i, community in enumerate(partition):
        print(f"Community {i} : {community}")

    colors = {}
    color_list = ["red", "blue", "green", "yellow", "purple", "orange"]
    for i, community in enumerate(partition):
        for vertex in community:
            colors[vertex] = color_list[i % len(color_list)]

    karate_graph.plot(
        labels=True,
        colors=[colors[v] for v in karate_graph.vertices]
    )
