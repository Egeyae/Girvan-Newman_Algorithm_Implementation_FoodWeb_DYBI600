import Graph as g
import csv 

def load_karate():
    """
        Function to load the karate club dataset. Will return the graph and the groups in the graph.
    """

    # Initilaze dict and graph.
    groups = {}
    karate_graph = g.Graph(name="Karate dataset")

    #Open the first csv file where the vertices are in.
    with open("data/Karate_club_dataset/nodes.csv") as fnodes:
        nodes = csv.reader(fnodes)

        #Skip the first line with the columns names.
        next(nodes)

        #For each line :
        for line in nodes:
            #Add the vertex.
            karate_graph.add_vertex(line[1])

            #Add in which community is in.
            if line[2] not in groups.keys():
                groups[line[2]] = [line[1]]
            else :
                groups[line[2]].append(line[1])
    
    #Open the second csv file with the edges.
    with open("data/Karate_club_dataset/edges.csv") as fedges :
        edges = csv.reader(fedges)

        #Skip the first line with the columns names.
        next(edges)
        # For each line :
        for line in edges:

            #Add the edge with + 1, because in the file index are used and not name.
            karate_graph.add_edge(str(int(line[0])+1), str(int(line[1])+1))
    
    return karate_graph, groups


if __name__ == "__main__":            
    karate_graph, groups = load_karate()

    karate_graph.plot()
