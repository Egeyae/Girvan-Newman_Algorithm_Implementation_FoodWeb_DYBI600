import matplotlib.pyplot as plt
from random import random
class Graph :
    """
    Class used to represent a Graph in our project
    Uses Adjacency Lists to save neighbors

    Later all functions implemented to run Girvan-Newman algorithm on graphs are based on this class
    """
    def __init__(self):
        """
        This function initialize the variable of the Graph.
        """

        self.nb_vertices = 0  #How many vertices in the graph 
        self.vertices = [] # The vertices of the graph, str type
        self.neighborhoods = [] # The neighborhoods of each vertex of the graph

    def __str__(self):
        s = f"Size: {self.nb_vertices}\n"
        for i in range(self.nb_vertices):
            s += f"[{i}] {self.vertices[i]} : {', '.join([str(x) for x in self.neighborhoods[i]])}\n"
        return s

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
        self.neighborhoods.append(set())
        self.nb_vertices += 1
        print("The vertex is added.") # To comment if not in verbose mode
    
    def remove_vertex(self,vertex):
        """
        Function to remove a vertex to the graph.
        Args :
            vertex : The vertex we want to add, type = str.
        """
        # We check is the vertex is not already removed of the graph.
        self._check_vertex(vertex)

        index = self.vertices.index(vertex)

        # If it's not the case, we remove the vertex of the list of vertices and we substract one to the numbers of vertices.
        self.vertices.pop(index)
        self.neighborhoods.pop(index)

        self.nb_vertices -= 1

        
        for i in range(self.nb_vertices):
            self.neighborhoods[i].discard(index)
            self.neighborhoods[i] = {n-1 if n>index else n for n in self.neighborhoods[i]}
            

        

    def add_edge(self, vertex1,vertex2):
        """
        Function to add an edge between two vertices.
        Args :
            vertex1, vertex 2 : The two vertices, type = str. 
        """
        # We check if both of the vertices are in the graph.
        self._check_vertex(vertex1)
        self._check_vertex(vertex2)

        #If it's not the case, we add the edge. 
        self.neighborhoods[self.vertices.index(vertex1)].add(self.vertices.index(vertex2))
        self.neighborhoods[self.vertices.index(vertex2)].add(self.vertices.index(vertex1))
    
    def remove_edge(self, vertex1, vertex2):
        """
        Function to remove an edge between two vertices.
        Args :
            vertex1, vertex 2 : The two vertices, type = str. 
        """
        # We check if both of the vertices are in the graph.
        self._check_vertex(vertex1)
        self._check_vertex(vertex2)

        #If it's not the case, we remove the edge. 
        self.neighborhoods[self.vertices.index(vertex1)].remove(self.vertices.index(vertex2))
        self.neighborhoods[self.vertices.index(vertex2)].remove(self.vertices.index(vertex1))
    
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
        Function to get the length of the neighborhood of a vertex.
        Args :
            vertex : The vertex we want to know the length neighborhood, type = str.
        """
        # We check is the vertex is in the graph.
        self._check_vertex(vertex)

        # We return the legnht of neighborhood
        return len(self.neighborhoods[self.vertices.index(vertex)])
    
    def get_vertex(self, index):
        """
        Function to get the vertex by it's index.
        Args :
            index = The index of the vertex we want to get.
        """
        if index >= self.nb_vertices:
            raise IndexError(f"{index} is invalid ! (Should be < {self.nb_vertices})")
        
        return self.vertices[index]
    
    def plot(self, k: int = 5000, desired: float = 0.2, repulsion: float = 0.1,
          attraction: float = 0.1, title: str = "Graph plot",
          output: str = None, show: bool = True):
        """
        Compute positions then save and/or show the resulting plot

        Args:
            k: number of iterations
            desired: desired distance between neighbors
            repulsion: repulsion force
            attraction: attraction force
            title: graph title
            output: if provided, saves the plot to specified file
            show: if True, display the graph (by default = True)
        """
        positions = [[random(), random()] for _ in range(self.nb_vertices)]
        all_vertices = set(range(self.nb_vertices))

        for _ in range(k):
            change_vectors = [[] for _ in range(self.nb_vertices)]
            for i in range(self.nb_vertices):
                neighbors = self.neighborhoods[i]
                not_neighbors = all_vertices - neighbors - {i}

                # Repulsion
                for j in not_neighbors:
                    dx = positions[i][0] - positions[j][0]
                    dy = positions[i][1] - positions[j][1]
                    dist = max(0.01, (dx**2 + dy**2)**0.5)
                    force = repulsion / dist**2
                    change_vectors[i].append([dx/dist * force, dy/dist * force])

                # Attraction
                for j in neighbors:
                    dx = positions[i][0] - positions[j][0]
                    dy = positions[i][1] - positions[j][1]
                    dist = max(0.01, (dx**2 + dy**2)**0.5)
                    force = attraction * (dist - desired)
                    change_vectors[i].append([-dx/dist * force, -dy/dist * force])

            for i in range(self.nb_vertices):
                final_dx = sum(v[0] for v in change_vectors[i])
                final_dy = sum(v[1] for v in change_vectors[i])
                positions[i][0] += final_dx * 0.01
                positions[i][1] += final_dy * 0.01

        x = [pos[0] for pos in positions]
        y = [pos[1] for pos in positions]

        fig, ax = plt.subplots()

        ax.scatter(x, y)
        for i in range(self.nb_vertices):
            for j in self.neighborhoods[i]:
                ax.plot([x[i], x[j]], [y[i], y[j]], 'k-')
        ax.set_title(title)

        if output:
            fig.savefig(output, dpi=300, bbox_inches='tight')
            plt.close(fig)
        if show:
            plt.show()
    