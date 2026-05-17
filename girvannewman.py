from Graph import Graph

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

    for vertex in range(g_original.get_vertices):
        degrees[vertex] = g_original.get_length_neighborhood(vertex)

    communitie_part ={}
    for index, community in enumerate(partition):
        for vertex in community :
            communitie_part[vertex] = index

    Q = 0

    for i in range(g_original.nb_edges):
        for j in range(g_original.nb_edges) :
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
            

def _modularity(g: Graph):
    pass


def _dendrogram(g: Graph):
    pass

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



    # print(list(set(("1", "2"))))
    # print(list(set(("2", "1"))))


    # for e,c in sorted(brandes(g).items(), key=lambda x: x[1]):
    #     print(f"{e} = {c}")

    # g.plot(labels=True)

    from loader import load_karate

    karate_graph, groups = load_karate()

    for e,c in sorted(brandes(karate_graph).items(), key=lambda x: x[1]):
        print(f"{e} = {c}")

    karate_graph.plot(labels=True)
