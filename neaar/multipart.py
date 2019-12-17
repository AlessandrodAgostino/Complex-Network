import networkx as nx
import random



G = nx.complete_multipartite_graph(1,2,3)



nx.write_gexf(G,"multipartite.gexf")


from neaar import pa_utils as pa
from networkx import read_gexf as rgexf
from arango import ArangoClient

host, username, password = pa.load_pass(filename='config.json')

# Initialize the client for ArangoDB. Connect to "_system" database as root user.
client = ArangoClient(hosts=host)
db     = client.db('_system', username=username, password=password)


arango, n = pa.read_gexf(db, "../data/multipartite.gexf")
nodes = arango.vertex_collection("nodes")
cursor = nodes.export()
nodes = cursor.batch()
nodes


#%%
nx_graph = rgexf("../data/multipartite.gexf")
import networkx as nx
nx.draw(nx_graph)
