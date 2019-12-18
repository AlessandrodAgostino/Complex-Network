import networkx as nx
import random
from neaar import pa_utils as pa
from networkx import read_gexf as rgexf
from arango import ArangoClient
import unidecode


host, username, password = pa.load_pass(filename='Complex-Network/config.json')
# Initializ the client for ArangoDB. Connect to "_system" database as root user.
client = ArangoClient(hosts=host)
db     = client.db('_system', username=username, password=password)


#%%
nx_graph = rgexf("data/multipartite.gexf")
graph      = nx.node_link_data(nx_graph)

nodes = list(nx_graph.nodes(data=True))

edges = list(nx_graph.edges(data= True))
edges

import numpy as np
format_len_link = int(np.log10(len(graph['links'])))


for n,link in enumerate(graph["links"]):
    print(graph["nodes"][n] == link["source"])


for n,link in enumerate(graph['links']):
  link['_key']  = f'E{n:{0}{format_len_link}}'
  link['_to']   = "collection_"+str(n[1]["subset"]) +'/' + unidecode.unidecode(str(link['target']))
  link['_from'] = "collection_"+str(n[1]["subset"]) +'/' + unidecode.unidecode(str(link['source']))

for n in nodes:
    collection_name = "collection_"+str(n[1]["subset"])
    nodes_collection = pa.check_create_empty_collection(db, collection_name)
    n[1]['_key'] = unidecode.unidecode(str(n[1]['label']))
    nodes_collection.insert(n)

edges_collection = pa.check_create_empty_collection(db=db,collection_name = "edges", edge=True)
edges_collection.insert_many(graph["links"])


