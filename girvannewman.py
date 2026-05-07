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


def _modularity(g: Graph):

    v_visited = set()
    community_members = []

    for vertex in g.vertices :
        if vertex in v_visited :
            continue 

        members = []
        queue = [vertex]

        while queue :
            v = queue.pop(0)
            if v in v_visited : 
                continue 
            v_visited.add(v)
            members.append(v)

            for neighbor in g.get_neighborhood(v):
                if neighbor not in v_visited : 
                    queue.append(neighbor)
        community_members.append(members)
    
    m = g.nb_edges
    if m == 0 :
        return 0
    
    edge_contribution = 0
    degree_tex = 0

    for members in community_members : 
        members_set = set(members)

        e_A = 0
        for v in members : 
            for neighbor in g.get_neighborhood(v):
                if neighbor in members_set : 
                    e_A += 1
        vol_A = sum(g.get_length_neighborhood(v) for v in members)

        edge_contribution += e_A
        degree_tex += vol_A ** 2
    return((edge_contribution/m) - (degree_tex / (4*m*m)))


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
