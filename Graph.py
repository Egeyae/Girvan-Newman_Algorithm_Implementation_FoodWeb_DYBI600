class Graph :

    def __init__(self):
        """
        This function initialize the variable of the Graph. 
        """

        self.nb_vertices = 0  #How many vertices in the graph 
        self.vertices = [] # The vertices of the graph, str type
        self.neighborhoods = [] # The neighborhoods of each vertex of the graph

    def _check_vertex(self,vertex,t="out"):
        """
        Check and raise a error depending of the setting.
        Args :
            vertex : The vertex we want to check, type = str. 
            t : If t = out, we want to check if the vertex is not in the graph and if yes raise an error,
            t = in we want to check if the vertex is in the graph and if yes, raise an error.
        """
        if t == "out" and vertex not in self.vertices :
            raise ValueError("The vertex is not in the vertices of the graph.")
        if t =="in" and vertex in self.vertices:
            raise ValueError("The vertex is already in the graph.")

    def add_vertex(self, vertex):
        """
        Function to add a vertex to the graph.
        Args :
            vertex : The vertex we want to add, type = str.
        """
        # We check is the vertex is not already in the graph.
        self._check_vertex(vertex, t="in")

        # If it's not the case, we add the vertex to the list of vertices and we add one to the numbers of vertices.
        self.vertices.append(vertex)
        self.nb_vertices += 1
        print("The vertex is added.") # To comment if not in verbose mode
    
    def remove_vertex(self, vertex):
        """
        Function to remove a vertex to the graph.
        Args :
            vertex : The vertex we want to add, type = str.
        """
        # We check is the vertex is not already removed of the graph.
        self._check_vertex(vertex)

        # If it's not the case, we remove the vertex of the list of vertices and we substract one to the numbers of vertices.
        self.vertices.pop(self.vertices.index(vertex))
        self.nb_vertices -= 1

    def add_edge(self, vertex,neighbor):
        """
        Function to add a vertex to the neighborhood of an another vertex.
        Args :
            vertex : The vertex we want to add the neighbor, type = str.
            neighbor : The vertex we xant 
        """
        # We check is the vertex and the neighbor is in of the graph.
        self._check_vertex(vertex)
        self._check_vertex(neighbor)

        #If it's noy the case, we add the neighbor to the neighborhood of the vertex and vice-versa. 
        self.neighborhoods[self.vertices.index(vertex)].add(self.vertices.index(neighbor))
        self.neighborhoods[self.vertices.index(neighbor)].add(self.vertices.index(vertex))
    
    def remove_neighbor(self, vertex, neighbor):
        """
        Function to remove a vertex to the neighborhood of an another vertex.
        Args :
            vertex : The vertex we want to remove the neighbor, type = str.
            neighbor : The vertex we want to remove 
        """
        # We check is the vertex and the neighbor is in of the graph.
        self._check_vertex(vertex)
        self._check_vertex(neighbor)

        #If it's noy the case, we remove the neighbor to the neighborhood of the vertex and vice-versa. 
        self.neighborhoods[self.vertices.index(vertex)].remove(self.vertices.index(neighbor))
        self.neighborhoods[self.vertices.index(neighbor)].remove(self.vertices.index(vertex))
    
    def get_neighborhood(self, vertex):
        """
        Function to get the neighborhood of a vertex.
        Args :
            vertex : The vertex we want to know the neighborhood, type = str.
        """
        # We check is the vertex is in the graph.
        self._check_vertex(vertex)

        # We return the neighborhood
        return self.neighborhoods[self.vertices.index(vertex)]
        
    def get_length_neighborhood(self,vertex):
        """
        Function to get the legth of the neighborhood of a vertex.
        Args :
            vertex : The vertex we want to know the length neighborhood, type = str.
        """
        # We check is the vertex is in the graph.
        self._check_vertex(vertex)

        # We return the legnht of neighborhood
        return len(self.neighborhoods[self.vertices.index(vertex)])
    