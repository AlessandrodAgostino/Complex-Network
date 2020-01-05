import random

import networkx as nx
from networkx import read_gexf as rgexf
from arango import ArangoClient
import unidecode
import numpy as np

from neaar import pa_utils as pa

host, username, password = pa.load_pass(filename='../config.json')
# Initializ the client for ArangoDB. Connect to "_system" database as root user.
client = ArangoClient(hosts=host)
db     = client.db('_system', username=username, password=password)

#%%

nx_graph = rgexf('../data/multipartite.gexf')
graph    = nx.node_link_data(nx_graph)

nodes = list(nx_graph.nodes(data=True))

edges = list(nx_graph.edges(data= True))

nodes[int(edges[0][0])][1]['subset']

classes = {}

for n,data in nx_graph.nodes(data=True):
    collection_name = 'collection_'+str(data['subset'])
    nodes_collection = pa.check_create_empty_collection(db, collection_name, truncate = False)
    data['_key'] = unidecode.unidecode(str(data['label']))
    nodes_collection.insert(data)
    classes[str(data['subset'])] = 'collection_'+str(data['subset'])

for n,ed in enumerate(nx_graph.edges(data=True)):
    graph['links'][n]['_key']  = 'E'+str(n)
    graph['links'][n]['_from'] =  classes[str(nodes[int(edges[n][0])][1]['subset'])]+'/'+str(edges[n][0])
    graph['links'][n]['_to']   =  classes[str(nodes[int(edges[n][1])][1]['subset'])]+'/'+str(edges[n][1])



#
# for n,link in enumerate(graph['links']):
#   link['_key']  = f'E{n:{0}{format_len_link}}'
#   link['_to']   = "collection_"+str(n[1]["subset"]) +'/' + unidecode.unidecode(str(link['target']))
#   link['_from'] = "collection_"+str(n[1]["subset"]) +'/' + unidecode.unidecode(str(link['source']))
#

edges_collection = pa.check_create_empty_collection(db=db,collection_name = "edges", edge=True)
edges_collection.insert_many(graph["links"])

dict(edges_collection)
# Directly create the graph and add egde collection
net = pa.check_create_empty_graph(db=db, graph_name="multipartite")
net.create_edge_definition("edges", ["collection_0","collection_1","collection_2"],["collection_0","collection_1","collection_2"])
