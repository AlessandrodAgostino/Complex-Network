import os
import json
from math import log
import networkx as nx
from networkx.readwrite.json_graph import node_link_data

#%% Loading Graph path
path       = os.path.join(os.path.dirname('__file__'), 'data', 'SymptomsNet.gexf')
graph      = nx.read_gexf(path)
nodes_list = list(graph.nodes())

json_graph = node_link_data(graph)

#Future name for Arango vertex collection
collection_name = 'Sym_Deas'

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
