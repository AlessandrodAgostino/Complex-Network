import os

from arango import ArangoClient

import script.pa_utils as pa

# Initialize the client for ArangoDB. Connect to "_system" database as root user.
client = ArangoClient(hosts='http://127.0.0.1:8529')
db     = client.db('_system', username='root', password=pa.load_pass('script/pwd.txt', isjson=False ))

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
astenia_first_neighbours
