from arango import ArangoClient
import json
import script.pythonarango as pa
import script.Ale_adb_import as adb

# Initialize the client for ArangoDB. Connect to "_system" database as root user.
client = ArangoClient(hosts='http://127.0.0.1:8529')
db     = client.db('_system', username='root', password=pa.load_pass('script/pwd.txt', isjson=False ))

# Only if u don't have the collections
Sym_Net = adb.read_gexf(db, filename='data/SymptomsNet.gexf',
                        nodes_collection_name='Sym_Deas',
                        edges_collection_name='Sym_Deas_edges',
                        graph_name='Sym_Net')

def traverse(db, starting_node, nodes_collection_name, graph_name, **kwargs):
  '''
  This function is basically a wrap of the traverse function of python-arango.
  The only difference is that it let you choose the starting node by its name.

  Parameters :
    db : Arango databases, result of the function client.db of python-arango
    starting_node : string, name of the starting node from which the travers starts.
    nodes_collection_name : string, name of the collection of nodes from which the
                            informations on "starting_node" are taken.
    graph_name : string, name of the graph in which the traverse is performed.
    **kwargs   : dictionary of all the arguments that python-arango traverse may accept
                 see :
                 https://python-driver-for-arangodb.readthedocs.io/en/master/graph.html
                 or :
                 https://python-driver-for-arangodb.readthedocs.io/en/master/specs.html#arango.graph.Graph.traverse
                 for reference.

  Returns:
    Python list containing
  '''

  node = pa.get_vertex(db, {'label' : f'{starting_node}'}, f'{nodes_collection_name}')
  Net  = db.graph(graph_name)

  result = Net.traverse(node, **kwargs)

  return result

# traversal
neighbours = traverse(db=db, starting_node='astenia',
                      nodes_collection_name='Sym_Deas', graph_name='Sym_Net',
                      direction        ='outbound',
                      item_order       ='forward',
                      min_depth        = 0,
                      max_depth        = 1,
                      vertex_uniqueness='global')

# create empty
pa.check_create_empty_collection(db, 'Sub_Sym_Deas_edges', edge=True)

# From now on we select the correct edges.
for n in neighbours['vertices']:
  edges_of_n = Sym_Net.edge_collection('Sym_Deas_edges').edges(n, 'out')['edges']
  for ed in edges_of_n:
    outgoing_node = Sym_Net.vertex_collection('Sym_Deas').get(ed['_to'])
    if outgoing_node in neighbours['vertices']:
        db.collection('Sub_Sym_Deas_edges').insert(ed)

graph = pa.check_create_empty_graph(db, 'Sub_Net')

if not graph.has_edge_definition('Sub_Sym_Deas_edges'):
  graph.create_edge_definition('Sub_Sym_Deas_edges', ['Sym_Deas'], ['Sym_Deas'])
