import os

import networkx as nx
import pylab as plt
import numpy as np
path = os.path.join(os.path.dirname('__file__'), '..' ,'data', 'SymptomsNet.gexf')

graph = nx.read_gexf(path)

#%%
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
plt.plot(e, 'o')

np.sum(e[3:])
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

#%%

class1 = list()
class2 = list()
connectivity = dict(graph.adj.items())

for node in connectivity:
  connectivity[node] = list(connectivity[node])

for node in connectivity:

  if node not in class1 and node not in class2:
    class1.append(node)
    class2.extend(connectivity[node])

from collections import Counter

count = Counter(class2)


len(class1)
len(count)

len(count) + len(class1)

rep = 0
for i, node1 in enumerate(count.keys()):
  for node2 in count.keys()[i:]:
    if node1 != node2:
      if node2 in connectivity[node1]:
        rep += 1.


#%%
