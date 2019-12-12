from arango import ArangoClient
import json
import near.pa_utils as pa
#%%
# Initialize the client for ArangoDB.
client = ArangoClient(hosts='http://127.0.0.1:8529')

# Connect to "_system" database as root user.
db = client.db('_system', username='root', password=pa.load_pass('near/pwd.txt', isjson=False ))
if db.has_graph('Sym_Net'):
    Sym_Net = db.graph('Sym_Net')
else: Sym_Net = db.create_graph(name='Sym_Net')

if not Sym_Net.has_edge_definition('Sym_Deas_edges'):
    Sym_Net.create_edge_definition('Sym_Deas_edges', ['Sym_Deas'], ['Sym_Deas'])

# extracting node
res = get_vertex(db, filter={'name':'astenia'}, collection_name='Sym_Deas')

# traversal
neighbours = Sym_Net.traverse(res,
                              direction        ='outbound',
                              item_order       ='forward',
                              min_depth        = 1,
                              max_depth        = 1,
                              vertex_uniqueness='global',
                              edge_uniqueness='None')

edges = retrieve_unique_edges(neighbours['paths'])

# create a new graph with the extracted nodes.
astenia_nodes = check_create_empty_collection(db, 'astenia_edges', edge=True)

astenia_nodes.insert_many(edges)

Sub_net = check_create_empty_graph(db, 'Astenia_friends')

if not Sym_Net.has_edge_definition('astenia_edges'):
  Sym_Net.create_edge_definition('astenia_edges', ['Sym_Deas'], ['Sym_Deas'])
