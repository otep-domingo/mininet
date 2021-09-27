from __future__ import print_function
import networkx as nx
from networkx.readwrite import json_graph
import json

g = nx.Graph()
# Don't need to add nodes separately.
g.add_edge(1,2, capacity=10)  # add a "capacity" parameter
g.add_edge(1,3, capacity=10)  # can have any name you like
g.add_edge(2,3, capacity=15)
print("NetworkX version = {}".format(nx.__version__))
print("Graph nodes are: {}".format(g.nodes()))
print("Graph edges are: {}".format(g.edges(data=True)))
print("Is edge (2,1) in the graph? {}".format(g.has_edge(2,1)))
print("Is edge (3,2) in the graph? {}".format(g.has_edge(3,2)))
print("The capacity of edge (2,3) is {}".format(g[2][3]["capacity"]))
# print graph as a JSON string
print(json.dumps(json_graph.node_link_data(g),indent=4))
