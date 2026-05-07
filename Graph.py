import matplotlib.pyplot as plt
from random import random
from adjustText import adjust_text
from math import sqrt

class Graph :
    """
    Class used to represent a Graph in our project
    Uses Adjacency Lists to save neighbors

    Later all functions implemented to run Girvan-Newman algorithm on graphs are based on this class
    """
    def __init__(self, name: str = "Graph"):
        """
        This function initialize the variable of the Graph.
        """

        self.nb_vertices: int = 0  #How many vertices in the graph 
        self.nb_edges: int = 0
        self.vertices: list = [] # The vertices of the graph, str type
        self.neighborhoods: dict = {} # The neighborhoods of each vertex of the graph

        self._name: str = name

    def __str__(self) -> str:
        s = f"Size: {self.nb_vertices}\n"
        for i,v in enumerate(self.vertices):
            s += f"[{i}] {v} : {', '.join(self.neighborhoods[v])}\n"
        return s

    def get_name(self) -> str:
        return self._name

    def _check_vertex(self, vertex: str, t="out") -> None:
        """
        Check and raise an error depending of the setting.
        Args :
            vertex : The vertex we want to check, type = str. 
            t : If t = out, we want to check if the vertex is not in the graph and if yes raise an error,
            t = in we want to check if the vertex is in the graph and if yes, raise an error.
        """
        if t == "out" and vertex not in self.vertices :
            raise ValueError("The vertex is not in the vertices of the graph.")
        if t =="in" and vertex in self.vertices:
            raise ValueError("The vertex is already in the graph.")

    def add_vertex(self, vertex: str) -> None:
        """
        Function to add a vertex to the graph.
        Args :
            vertex : The vertex we want to add, type = str.
        """
        # We check is the vertex is not already in the graph.
        self._check_vertex(vertex, t="in")

        # If it's not the case, we add the vertex to the list of vertices and we add one to the numbers of vertices.
        self.vertices.append(vertex)
        self.neighborhoods[vertex] = set()
        self.nb_vertices += 1
    
    def remove_vertex(self, vertex: str) -> None:
        """
        Function to remove a vertex to the graph.
        Args :
            vertex : The vertex we want to add, type = str.
        """
        # We check is the vertex is not already removed of the graph.
        self._check_vertex(vertex)

        # If it's not the case, we remove the vertex of the list of vertices and we substract one to the numbers of vertices.
        self.vertices.remove(vertex)
        del self.neighborhoods[vertex]

        self.nb_vertices -= 1

        
        for v in self.vertices:
            self.neighborhoods[v].discard(vertex)

    def add_edge(self, vertex1: str, vertex2: str) -> None:
        """
        Function to add an edge between two vertices.
        Args :
            vertex1, vertex 2 : The two vertices, type = str. 
        """
        # We check if both of the vertices are in the graph.
        self._check_vertex(vertex1)
        self._check_vertex(vertex2)

        #If it's not the case, we add the edge. 
        self.neighborhoods[vertex1].add(vertex2)
        self.neighborhoods[vertex2].add(vertex1)

        self.nb_edges += 1
    
    def remove_edge(self, vertex1: str, vertex2: str) -> None:
        """
        Function to remove an edge between two vertices.
        Args :
            vertex1, vertex 2 : The two vertices, type = str. 
        """
        # We check if both of the vertices are in the graph.
        self._check_vertex(vertex1)
        self._check_vertex(vertex2)

        #If it's not the case, we remove the edge. 
        self.neighborhoods[vertex1].remove(vertex2)
        self.neighborhoods[vertex2].remove(vertex1)

        self.nb_edges -= 1
    
    def get_neighborhood(self, vertex: str) -> set:
        """
        Function to get the neighborhood of a vertex.
        Args :
            vertex : The vertex we want to know the neighborhood, type = str.
        """
        # We check is the vertex is in the graph.
        self._check_vertex(vertex)

        # We return the neighborhood
        return self.neighborhoods[vertex]
        
    def get_length_neighborhood(self, vertex: str) -> int:
        """
        Function to get the length of the neighborhood of a vertex.
        Args :
            vertex : The vertex we want to know the length neighborhood, type = str.
        """
        # We check is the vertex is in the graph.
        self._check_vertex(vertex)

        # We return the legnht of neighborhood
        return len(self.neighborhoods[vertex])
    
    def get_vertex(self, index: int) -> str:
        """
        Function to get the vertex by it's index.
        Args :
            index = The index of the vertex we want to get.
        """
        if index >= self.nb_vertices:
            raise IndexError(f"{index} is invalid ! (Should be < {self.nb_vertices})")
        
        return self.vertices[index]

    def get_index(self, vertex: str) -> int:
        """
        Function to get the index of a given vertex
        Args:
            vertex = Name of the vertex
        """
        self._check_vertex(vertex)

        return self.vertices.index(vertex)
    
    def plot(self, k: int = 2500, desired: float = 0.15, repulsion: float = 0.2,
          attraction: float = 0.2, title: str|None = None, labels: bool = False, colors: list|None = None,
          output: str|None = None, show: bool = True):
        """
        Compute positions then save and/or show the resulting plot

        Args:
            k: number of iterations
            desired: desired distance between neighbors
            repulsion: repulsion force
            attraction: attraction force
            title: graph title, by default is the name of the Graph()
            output: if provided, saves the plot to specified file
            show: if True, display the graph (by default = True)
        """

        # We first put all vertices in random positions 
        positions = [[random(), random()] for _ in range(self.nb_vertices)]

        # We use a set to easily get the neighbors and the non neighbors vertices
        all_vertices = set(self.vertices)
        t = title or self._name

        # How much we should change the points each iterations
        change_vectors = [[0.0, 0.0] for _ in range(self.nb_vertices)]

        # Loop k iterations
        for _ in range(k):
            # Set the change vectors to 0, less computational intensive that creating a new list each time
            for i in range(self.nb_vertices):
                change_vectors[i][0] = 0.0
                change_vectors[i][1] = 0.0

            # For each vertex we compute its change vector
            for i,vi in enumerate(self.vertices):
                neighbors = self.neighborhoods[vi]
                not_neighbors = all_vertices - neighbors - {vi}

                # Repulsion
                for nn in not_neighbors:
                    j = self.get_index(nn)
                    dx = positions[i][0] - positions[j][0]
                    dy = positions[i][1] - positions[j][1]
                    dist2 = max(0.001, (dx*dx + dy*dy))
                    dist = sqrt(dist2)
                    force = repulsion / dist2
                    change_vectors[i][0] += dx/dist * force * 0.1
                    change_vectors[i][1] += dy/dist * force * 0.1

                # Attraction
                for n in neighbors:
                    j = self.get_index(n)
                    dx = positions[i][0] - positions[j][0]
                    dy = positions[i][1] - positions[j][1]
                    dist = max(0.01, sqrt((dx*dx + dy*dy)))
                    force = attraction * (dist - desired)
                    change_vectors[i][0] += -dx/dist * force * 0.1
                    change_vectors[i][1] += -dy/dist * force * 0.1

            for i in range(self.nb_vertices):
                positions[i][0] += change_vectors[i][0]
                positions[i][1] += change_vectors[i][1]

        x = [pos[0] for pos in positions]
        y = [pos[1] for pos in positions]

        fig, ax = plt.subplots()

        col = colors or ['blue' for _ in range(self.nb_vertices)]
        
        ax.scatter(x, y, c=col, s=40)

        for i, vi in enumerate(self.vertices):
            for vj in self.neighborhoods[vi]:
                j = self.get_index(vj)
                ax.plot([x[i], x[j]], [y[i], y[j]], 'k-', alpha=0.2)

        ax.set_title(t)
        if labels:
            ax = [ax.annotate(txt, (x[i],y[i])) for i, txt in enumerate(self.vertices)]
            adjust_text(ax)

        if labels:
            ax = [ax.annotate(txt, (x[i],y[i])) for i, txt in enumerate(self.vertices)]
            adjust_text(ax)

        if output:
            fig.savefig(output, dpi=300, bbox_inches='tight')
            plt.close(fig)
        if show:
            plt.show()
    