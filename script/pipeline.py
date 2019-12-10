import os

from arango import ArangoClient

import script.pa_utils as pa

# Initialize the client for ArangoDB. Connect to "_system" database as root user.
client = ArangoClient(hosts='http://127.0.0.1:8529')
db     = client.db('_system', username='root', password=pa.load_pass('script/pwd.txt', isjson=False ))

# Only if u don't have the collections
Sym_Net = pa.read_gexf(db, filename='data/SymptomsNet.gexf',
                        nodes_collection_name='Sym_Deas',
                        edges_collection_name='Sym_Deas_edges',
                        graph_name='Sym_Net')

# file path
path = os.path.join(os.path.dirname('__file__'), 'data', 'SymptomsNet.gexf')

# load graph and collections from file gexf, return graph object
graph = pa.read_gexf(db, filename='data/SymptomsNet.gexf',
          nodes_collection_name='Sym_Deas',                 #create a node collection named Sym_Deas
          edges_collection_name='Sym_Deas_edges',           #create an edge collection named Sym_Deas_edges
          graph_name='Sym_Net')                             #create a graph named Sym_Net

#now in the Arango web interface we have a graph and the two collections of nodes and edges.


# extract a subnet from the graph with a graph traverse of python-arango
# This could be any traversal, any query, any sub set of nodes from Sym_Deas
astenia_first_neighbours = pa.traverse(db=db, starting_node='astenia',
                                       nodes_collection_name='Sym_Deas',
                                       graph_name='Sym_Net',
                                       direction='outbound',
                                       item_order='forward',
                                       min_depth=0,
                                       max_depth=1,
                                       vertex_uniqueness='global')

#now we have a dict of the first neighbours of astenia and all the paths which reach that neighbour
astenia_first_neighbours.keys()

# create empty collection for the subnet
pa.check_create_empty_collection(db, 'Sub_Sym_Deas_edges', edge=True)

# We select only the edges that starts and ends within the sub net vertex set.
# All the sub net's information is hence contained in this new edge collection.
for n in astenia_first_neighbours['vertices']:
  edges_of_n = Sym_Net.edge_collection('Sym_Deas_edges').edges(n, 'out')['edges']
  for ed in edges_of_n:
    outgoing_node = Sym_Net.vertex_collection('Sym_Deas').get(ed['_to'])
    if outgoing_node in astenia_first_neighbours['vertices']:
        db.collection('Sub_Sym_Deas_edges').insert(ed)

#Check and create the sub graph with the new edge definition.
graph = pa.check_create_empty_graph(db, 'Sub_Net')
if not graph.has_edge_definition('Sub_Sym_Deas_edges'):
  graph.create_edge_definition('Sub_Sym_Deas_edges', ['Sym_Deas'], ['Sym_Deas'])

#now networkx for analysis
import networkx as nx

#exporting nodes and edges directly from the graph of pythonarango
edges = db.graph('Sub_Net').edge_collection("Sub_Sym_Deas_edges")
nodes = db.graph('Sub_Net').vertex_collections()#("Sub_Sym_Deas_edges")

#export dicts of edges
cursor = edges.export()
g = cursor.batch()

#networkx wants an edgelist definition for the graph
# create edge list and load graph
links = [f"{ed['source']} {ed['target']}" for ed in g]
G = nx.read_edgelist(links)

# add nodes attributes directly from from Sym_Deas
for node in G.nodes():
  attr = pa.get_vertex(db, {'label':node}, 'Sym_Deas')
  nx.set_node_attributes(G, {node : attr})

nx.draw(G)
