import os

import networkx as nx
import pylab as plt
import numpy as np
path = os.path.join(os.path.dirname('__file__'), 'data', 'directed_SymptomsNet.gexf')

graph = nx.read_gexf(path)


len(graph.nodes)
graph.nodes()
len(graph.edges)
first = list(graph.nodes)[0]
first
len(graph.adj[first])
graph.adj.items()
sp = dict(nx.all_pairs_shortest_path(graph))

graph.degree()

A = nx.adjacency_matrix(graph)

A = nx.to_numpy_matrix(graph)
print(A)
e = np.linalg.eigvals(A)
plt.plot(e)
np.sum(e)
plt.imshow(np.matrix(A))
nx.degree_centrality(graph)

graph.edges()

nx.bipartite.is_bipartite(graph)
nx.is_directed(graph)
graph.remove_edge(graph.nodes)

plt.figure(dpi = 200)
plt.imshow(A*A)
plt.show()
#%%


bottom_nodes, top_nodes = nx.bipartite.sets(graph)


B = nx.Graph()
# Add nodes with the node attribute "bipartite"
B.add_nodes_from([1, 2, 3, 4], bipartite=0)
B.add_nodes_from(['a', 'b', 'c'], bipartite=1)
# Add edges only between nodes of opposite node sets
B.add_edges_from([(1, 'a'), (1, 'b'), (2, 'b'), (2, 'c'), (3, 'c'), (4, 'a')])

A = nx.to_numpy_matrix(B)
plt.imshow(A)
nx.write_gexf(B,"bipartite.gexf")
