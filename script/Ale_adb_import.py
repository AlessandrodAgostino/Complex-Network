import os
import json
from math import log

import networkx as nx
from networkx.readwrite.json_graph import node_link_data

import script.pythonarango as pa
from arango import ArangoClient

#%% Loading Graph path
path       = os.path.join(os.path.dirname('__file__'), 'data', 'SymptomsNet.gexf')
graph      = nx.read_gexf(path)
nodes_list = list(graph.nodes())
json_graph = node_link_data(graph)

#Future name for Arango vertex collection
nodes_collection_name = 'Sym_Deas'
edges_collection_name = nodes_collection_name + '_edges'

# Number of digit needed for counting the nodes
format_len_node = round(log(len(json_graph['nodes']),10)) + 1

# Adding required '_key' attribute for Arango managing
for n,node in enumerate(json_graph['nodes']):
  node['_key'] = 'N{}'.format(str(n).zfill(format_len_node)) #Padding in format N0001

# Number of digit needed for counting the links
format_len_link = round(log(len(json_graph['links']),10)) + 1

# Adding required '_key', '_to', '_from' attribute for Arango managing
for n,link in enumerate(json_graph['links']):
  link['_key']  = 'E{}'.format(str(n).zfill(format_len_link))
  link['_to']   = '{}/N{}'.format(collection_name, str(nodes_list.index(link['target'])).zfill(format_len_node))
  link['_from'] = '{}/N{}'.format(collection_name, str(nodes_list.index(link['source'])).zfill(format_len_node))

# Build a collection. insert_many after check_create_empty_collection with apropriate name

# Initialize the client for ArangoDB.
client = ArangoClient(hosts='http://127.0.0.1:8529')

# Connect to "_system" database as root user.
db = client.db('_system', username='root', password=pa.load_pass('script/pwd.txt', isjson=False ))

# Create nodes collection and insert all the nodes in the net
Sym_Deas = pa.check_create_empty_collection(db=db, collection_name=nodes_collection_name, edge=False)
Sym_Deas.insert_many(json_graph['nodes'])

# Create links collection and inser all the edges in the net
Sym_Deas_edges = pa.check_create_empty_collection(db=db, collection_name=edges_collection_name, edge=True)
Sym_Deas_edges.insert_many(json_graph['links'])

# Directly create the graph and add egde collection
Sym_Net = pa.check_create_empty_graph(db=db, graph_name='Sym_Net')
Sym_Net.create_edge_definition(edges_collection_name, [nodes_collection_name], [nodes_collection_name])
