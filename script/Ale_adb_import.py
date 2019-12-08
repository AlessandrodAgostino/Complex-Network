import os
import json
from math import log, ceil

from networkx import read_gexf as rgexf
from networkx.readwrite import node_link_data

from arango import ArangoClient
import script.pythonarango as pa

def read_gexf(db, filename, nodes_collection_name='nodes', edges_collection_name='edges', graph_name='Net'):
  '''
  Creates a graph on arangodb from a gexf file. Requires networkx to be installed.

  Read the graph with the function read_gexf of networkx and generates a json formatted with
  node_link_data, containing

  Parameters:
    db       : Arango databases, result of the function client.db of python-arango
    filename : string, name of the .gexf file to be read
    nodes_collection_name : string, default "nodes". Name of the collection in which nodes
                            informations are stored. Carefull, if the collection already exists,
                            it will be truncated.
    edges_collection_name : string, default "edges". Name of the collection in which edges
                            informations are stored. Carefull, if the collection already exists,
                            it will be truncated.
    graph_name : string, default "Net". Name of the graph created from the collections.
                 Carefull, if the graph already exists, it will be overwritten.

  Returns:
    graph object of python-arango
  '''

  graph      = rgexf(filename)
  nodes_list = list(graph.nodes())   # needed for link document creation
  graph      = node_link_data(graph) # override graph, is not usefull anymore here

  # Number of digit needed for counting the nodes:
  format_len_node = ceil(log(len(graph['nodes']),10))
  # Number of digit needed for counting the links:
  format_len_link = ceil(log(len(graph['links']),10))

  # Adding required '_key' attribute for Arango managing
  for n,node in enumerate(graph['nodes']):
    # node['_key'] = 'N{n:{fill}{width}}'.format(n=n, fill='0', width=format_len_node) #Padding in format N0001, with style
    # the line above doesn't work for python 3.6 (RICHI ARGH), so:
    node['_key'] = 'N{}'.format(str(n).zfill(format_len_node))

  # Adding required '_key', '_to', '_from' attribute for Arango managing
  for n,link in enumerate(graph['links']):
    link['_key']  = 'E{}'.format(str(n).zfill(format_len_link))
    link['_to']   = '{}/N{}'.format(nodes_collection_name, str(nodes_list.index(link['target'])).zfill(format_len_node))
    link['_from'] = '{}/N{}'.format(nodes_collection_name, str(nodes_list.index(link['source'])).zfill(format_len_node))

  # Create nodes collection and insert all the nodes in the net
  Sym_Deas = pa.check_create_empty_collection(db=db, collection_name=nodes_collection_name, edge=False)
  Sym_Deas.insert_many(graph['nodes'])

  # Create links collection and inser all the edges in the net
  Sym_Deas_edges = pa.check_create_empty_collection(db=db, collection_name=edges_collection_name, edge=True)
  Sym_Deas_edges.insert_many(graph['links'])

  # Directly create the graph and add egde collection
  Net = pa.check_create_empty_graph(db=db, graph_name=graph_name)
  Net.create_edge_definition(edges_collection_name, [nodes_collection_name], [nodes_collection_name])

  return Net

if __name__ == '__main__':

  # Initialize the client for ArangoDB. Connect to "_system" database as root user.
  client = ArangoClient(hosts='http://127.0.0.1:8529')
  db     = client.db('_system', username='root', password=pa.load_pass('script/pwd.txt', isjson=False ))

  # file path
  path = os.path.join(os.path.dirname('__file__'), 'data', 'SymptomsNet.gexf')

  read_gexf(db, filename='data/SymptomsNet.gexf',
            nodes_collection_name='Sym_Deas',
            edges_collection_name='Sym_Deas_edges',
            graph_name='Sym_Net')
