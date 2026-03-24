from Graph import Graph

g = Graph()

g.add_vertex("A")
g.add_vertex("B")
g.add_vertex("C")
g.add_vertex("D")
g.add_vertex("E")
g.add_vertex("F")
g.add_vertex("G")
g.add_vertex("H")
g.add_vertex("I")
g.add_vertex("J")
g.add_vertex("K")
g.add_vertex("L")
g.add_vertex("Z")
g.add_vertex("X")
g.add_vertex("Y")


g.add_edge("A","B")
g.add_edge("A","C")
g.add_edge("C","B")
g.add_edge("A","E")
g.add_edge("F","C")
g.add_edge("C","L")
g.add_edge("G","E")
g.add_edge("D","C")
g.add_edge("K","L")
g.add_edge("G","E")
g.add_edge("D","H")
g.add_edge("K","J")

g.add_edge("I","Z")
g.add_edge("I","X")
g.add_edge("I","Y")
g.add_edge("X","Z")




g.plot(k=5000)


