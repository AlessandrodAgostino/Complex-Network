import networkx as nx
from arango import ArangoClient
import script.pa_utils as pa
import matplotlib.pyplot as plt

import pandas as pd

client = ArangoClient(hosts='http://127.0.0.1:8529')
db     = client.db('_system', username='root', password=pa.load_pass('script/pwd.txt', isjson=False ))

graph = pa.check_create_empty_graph(db, 'Sub_Net')

if not graph.has_edge_definition('Sub_Sym_Deas_edges'):
  graph.create_edge_definition('Sub_Sym_Deas_edges', ['Sym_Deas'], ['Sym_Deas'])

edges = db.graph('Sub_Net').edge_collection("Sub_Sym_Deas_edges")
nodes = db.graph('Sub_Net').vertex_collections()#("Sub_Sym_Deas_edges")

cursor = edges.export()
g = cursor.batch()

links = [f"{ed['source']} {ed['target']}" for ed in g]

# for i in range(len(g)):
#     links.append(str(g[i]["source"])+" "+str(g[i]["target"]))

G = nx.read_edgelist(links)
nx.draw(G)
degree = list(G.degree())
G.nodes(True)

d = nx.degree(G)

#
# A = nx.convert_matrix.to_numpy_matrix(G)
# plt.imshow(A)
