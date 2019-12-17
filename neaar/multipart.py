import networkx as nx
import random
from neaar import pa_utils as pa
from networkx import read_gexf as rgexf
from arango import ArangoClient


host, username, password = pa.load_pass(filename='Complex-Network/config.json')
# Initializ the client for ArangoDB. Connect to "_system" database as root user.
client = ArangoClient(hosts=host)
db     = client.db('_system', username=username, password=password)


#%%
nx_graph = rgexf("data/multipartite.gexf")
nodes = list(nx_graph.nodes(data = True))

for n in nodes:
    collection_name = "collection_"+str(n[1]["subset"])
    pa.check_create_empty_collection(db, collection_name)
