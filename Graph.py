class Graph :

    def __init__(self):
        self.nb_vertices = 0
        self.vertices = []
        self.neighborhoods = []

    def add_vertex(self, vertex):
        if vertex in self.vertices:
            print("The vertex is already in the graph.")
        else:
            self.vertices.append(vertex)
            self.nb_vertices += 1
            print("The vertex is added.")
    
    def remove_vertex(self, vertex):
        

    def add_neighbor(self, vertex,neighbor):
        if neighbor not in self.vertices :
            print("The neighbor is not in the vertices")
        elif vertex not in self.vertex:
            print("The vertex is not in the vertices")
        else:
            self.neighborhoods[self.vertices.index(vertex)].add(self.vertices.index(neighbor))
    
