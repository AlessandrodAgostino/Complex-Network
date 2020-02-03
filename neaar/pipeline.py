import os

from arango import ArangoClient
import networkx as nx

from neaar import pa_utils as pa

'''
This file is a summary of what we are able to do by now:
  - load gexf file into networkx.
  - create two collections (edge, node) and a graph in any arango database for any user.
  - perform a query (traverse) on the graph (in arangodb from python)
    and select a sub-set of vertices.
  - create the sub network containing this subset.
  - export the sub network and load it into networkx (or whathever) for python analysis.

Problems:
  - The sub-net creation algorithm (the double for in the end) is a bit slow. (Solved with newtorkx Sub-Graph)
  - The sub-net visualization take all the vertices, so is not immediately centered. (Kind Solved with Sub-Graph)
'''

host, username, password = pa.load_pass(filename='config.json')

# Initialize the client for ArangoDB. Connect to "_system" database as root user.
client = ArangoClient(hosts=host)
db     = client.db('_system', username=username, password=password)

#%%
# path of the file where orinal data are stored
# in atom this is bit strange actually.
filename = os.path.join(os.path.dirname('__file__'), '..' ,'data', 'SymptomsNet.gexf')
filename= '../data/multipartite.gexf'
# This function read a gexf file and create two
# collections (edge, node) and a graph in database db.
Sym_Net, Nx_Net = pa.read_gexf(db, filename=filename,multipartite = True,
                       nodes_collection_name='Sym_Deas',
                       edges_collection_name='Sym_Deas_edges',
                       graph_name='Sym_Net')
# Now in the Arango web interface we have a graph and the two collections of nodes and edges.

# Extract a subnet from the graph with a graph traverse of python-arango
# This could be any traversal, any query, any sub set of nodes from Sym_Deas
astenia_first_neighbours = pa.traverse(db=db, starting_node='emicrania',
                                       nodes_collection_name='Sym_Deas',
                                       graph_name='Sym_Net',
                                       direction='outbound',
                                       item_order='forward',
                                       min_depth=0,
                                       max_depth=1,
                                       vertex_uniqueness='global')

# Now we have a dict of the first neighbours of astenia and all the paths which
# reach that neighbours

# Build the Sub_Net in networkx easy peasy
Nx_Sub_Net = Nx_Net.subgraph([vertex['label'] for vertex in astenia_first_neighbours['vertices']])

for node in Nx_Sub_Net:
  attr = pa.get_vertex(db, {'label':node}, 'Sym_Deas')
  nx.set_node_attributes(Nx_Sub_Net, {node : attr})

sub_net = nx.readwrite.node_link_data(Nx_Sub_Net)

sub_net = pa.nx_to_arango(sub_net, 'Sub_Net')

Sub_Net = pa.export_to_arango(db, sub_net ,'Sub_Net', 'Sub_Net_edges', 'Sub_Graph')

################### Keep this code as it is, may comes in handy later #########

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

# Check and create the sub graph with the new edge definition.
graph = pa.check_create_empty_graph(db, 'Sub_Net')
if not graph.has_edge_definition('Sub_Sym_Deas_edges'):
  graph.create_edge_definition('Sub_Sym_Deas_edges', ['Sym_Deas'], ['Sym_Deas'])

# now networkx for analysis
import networkx as nx

# export edges directly from the graph of pythonarango
edge_collection = db.graph('Sub_Net').edge_collection("Sub_Sym_Deas_edges")

# export dicts of edges
cursor = edge_collection.export()
edges  = cursor.batch()

# create edge list
links = [f"{ed['source']} {ed['target']}" for ed in edges]

# load graph
G = nx.read_edgelist(links)

# add nodes attributes directly from the original node collection
for node in G.nodes():
  attr = pa.get_vertex(db, {'label':node}, 'Sym_Deas')
  nx.set_node_attributes(G, {node : attr})

# Now we have a networkx (Sub) Graph object with all the informations stored
# in the arangodb collection
