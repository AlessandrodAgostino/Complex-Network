import random

import networkx as nx
from networkx import read_gexf as rgexf
from arango import ArangoClient
import unidecode
import numpy as np

from neaar import pa_utils as pa

host, username, password = pa.load_pass(filename='config.json')
# Initializ the client for ArangoDB. Connect to "_system" database as root user.
client = ArangoClient(hosts=host)
db     = client.db('_system', username=username, password=password)

#%%

nx_graph = rgexf('../data/multipartite.gexf')
graph    = nx.node_link_data(nx_graph)
nodes = list(nx_graph.nodes(data=True))
edges = list(nx_graph.edges(data= True))

classes = {}

#now insert each node in their collections
for n,data in nx_graph.nodes(data=True):
    collection_name = 'collection_'+str(data['subset'])
    nodes_collection = pa.check_create_empty_collection(db, collection_name, truncate = False)
    data['_key'] = unidecode.unidecode(str(data['label']))
    nodes_collection.insert(data)
    classes[data['subset']] = 'collection_'+str(data['subset'])

edges_collection = pa.check_create_empty_collection(db=db,collection_name = "edges", edge=True)

#now insert the edges in the edge collection and the attributes from and to with the right classes
for n,ed in enumerate(nx_graph.edges(data=True)):
    ed[2]['_key']  = 'E'+str(n)
    ed[2]['_from'] =  classes[nx_graph.nodes[ed[0]]['subset']] + '/' + str(ed[0])
    ed[2]['_to']   =  classes[nx_graph.nodes[ed[1]]['subset']] + '/' + str(ed[1])
    edges_collection.insert(ed[2])

net = pa.check_create_empty_graph(db=db, graph_name="multipartite")
net.create_edge_definition("edges", list(classes.values()),list(classes.values()))
