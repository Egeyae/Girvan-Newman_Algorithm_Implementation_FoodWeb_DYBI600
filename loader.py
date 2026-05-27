import Graph as g
import csv 

name_food_web = {0 : "Phytoplancton", 1 : "Suspended Bacteria",2 : "Sediment Bacteria", 3 : "Benthic diatoms", 4 : "Free bacteria", 5 : "Heterotrop^hic microflagellates", 6 : "Microzooplankton",7: "Zooplankton", 8: "Cnetophore", 9: "Sea nettle", 10 : "Other suspendfeeders", 11 : "Mya", 12 :"Oysters", 13 : "Other polychaetes", 14 : "Nereis"}

def load_karate():
    """
        Function to load the karate club dataset. Will return the graph and the groups in the graph.
    """

    # Initilaze dict and graph.
    groups = {}
    karate_graph = g.Graph(name="Karate dataset")

    # Open the first csv file where the vertices are in.
    with open("data/Karate_club_dataset/nodes.csv") as fnodes:
        nodes = csv.reader(fnodes)

        # Skip the first line with the columns names.
        next(nodes)

        # For each line :
        for line in nodes:
            # Add the vertex.
            karate_graph.add_vertex(line[1])

            # Add in which community is in.
            if line[2] not in groups.keys():
                groups[line[2]] = [line[1]]
            else :
                groups[line[2]].append(line[1])
    
    # Open the second csv file with the edges.
    with open("data/Karate_club_dataset/edges.csv") as fedges :
        edges = csv.reader(fedges)

        # Skip the first line with the columns names.
        next(edges)
        # For each line :
        for line in edges:

            # Add the edge with + 1, because in the file index are used and not name.
            karate_graph.add_edge(str(int(line[0])+1), str(int(line[1])+1))
    
    return karate_graph, groups

def load_college_football():
    """
        Function to load the college football network dataset. Will return the graph and the groups in the graph.
    """

    # Initilaze dict and graph.
    groups = {}
    college_football_graph = g.Graph(name="College_football_dataset")

    # Open the first csv file where the vertices are in.
    with open("data/NCAA_college_football_2000_dataset/nodes.csv") as fnodes:
        nodes = csv.reader(fnodes)
        next(nodes)

        # For each line : 
        for line in nodes:
            # Add the vertex.
            college_football_graph.add_vertex(line[1])

            # Add in which community is in.
            if line[2] not in groups.keys():
                groups[line[2]] = [line[1]]
            else :
                groups[line[2]].append(line[1])

    # Open the second csv file with the edges.

    with open("data/NCAA_college_football_2000_dataset/edges.csv") as fedges :
        edges = csv.reader(fedges)

        # Skip the first line with the columns names.
        next(edges)
        # For each line :
        for line in edges:
            # Add the edge with + 1, because in the file index are used and not name.
            college_football_graph.add_edge(college_football_graph.get_vertex(int(line[0])), college_football_graph.get_vertex(int(line[1])))
    
    return college_football_graph, groups

def load_data_food_web():
    """
        Function to load the cfoodweb dataset. Will return the graph.
    """
    foodweb_graph = g.Graph(name="FoodWeb")
    with open("data/Foodweb_data/Adj_Mat_Coefficient_Chart.txt") as fmat :
        lines  = fmat.readlines()
        assert len(lines) == 36, "Not the right count of vertices in the files."
        for i in range(len(lines)):
            line = lines[i].strip().split()
            
            assert int(line[0]) == i+1, "The index of i and the name of the vertex don't correspond."
            line = line[1:]
            assert len(line) == 36,"Not the right of vertices in the line."

        return 1

if __name__ == "__main__":            
    karate_graph, groups = load_karate()

    college_graph, groups2 = load_college_football()
    load_data_food_web()
    #print(groups2)
    #college_graph.plot()
    #karate_graph.plot(labels=True)
