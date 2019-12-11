import json

from arango import ArangoClient

import script.pa_utils as pa
import script.Ale_adb_import as adb

#%%
# Initialize the client for ArangoDB. Connect to "_system" database as root user.
client = ArangoClient(hosts='http://127.0.0.1:8529')
db     = client.db('_system', username='root', password=pa.load_pass('script/pwd.txt', isjson=False ))

# Only if u don't have the collections
Sym_Net = pa.read_gexf(db, filename='data/SymptomsNet.gexf',
                        nodes_collection_name='Sym_Deas',
                        edges_collection_name='Sym_Deas_edges',
                        graph_name='Sym_Net')

#%%
# This could be any traversal, any query, any sub set of nodes from Sym_Deas
neighbours = pa.traverse(db=db, starting_node='astenia',
                         nodes_collection_name='Sym_Deas', graph_name='Sym_Net',
                         direction        ='outbound',
                         item_order       ='forward',
                         min_depth        = 0,
                         max_depth        = 1,
                         vertex_uniqueness='global')
#%%
# create empty
pa.check_create_empty_collection(db, 'Sub_Sym_Deas_edges', edge=True)

# We select only the edges that starts and ends within the sub net vertex set.
# All the sub net's information is hence contained in this new edge collection.
for n in neighbours['vertices']:
  edges_of_n = Sym_Net.edge_collection('Sym_Deas_edges').edges(n, 'out')['edges']
  for ed in edges_of_n:
    outgoing_node = Sym_Net.vertex_collection('Sym_Deas').get(ed['_to'])
    if outgoing_node in neighbours['vertices']:
        db.collection('Sub_Sym_Deas_edges').insert(ed)

#Check and create the sub graph with the new edge definition.
graph = pa.check_create_empty_graph(db, 'Sub_Net')
if not graph.has_edge_definition('Sub_Sym_Deas_edges'):
  graph.create_edge_definition('Sub_Sym_Deas_edges', ['Sym_Deas'], ['Sym_Deas'])
