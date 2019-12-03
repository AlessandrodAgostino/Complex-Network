from arango import ArangoClient
import json
from script.pythonarango import check_create_empty_collection, check_create_empty_graph


def load_pass(filename, isjson=True):
  '''
  load password from a json file formatted like :
  {
    "username" : "root"
    "password" : "1234"
  }
  '''
  if isjson:
    with open(filename) as f:
      doc      = json.load(f)
      password = doc['password']
    return password
  else:
    with open(filename) as f:
      password = f.read()
      password = password[:-1]
    return password

def get_vertex(filter, collection_name):
  """
  filter : dictionary of conditions

  return: the document as dict
  """
  return db.collection(collection_name).find(filter).batch()[0]


# Initialize the client for ArangoDB.
client = ArangoClient(hosts='http://127.0.0.1:8529')

# Connect to "_system" database as root user.
db = client.db('_system', username='root', password=load_pass('script/pwd.txt', isjson=False ))

Sym_Net = check_create_empty_graph(db, 'Sym_Net')

Sym_Net.create_edge_definition('Sym_Deas_edges', ['Sym_Deas'], ['Sym_Deas'])

#extracting node
res = get_vertex({'name':'astenia'}, 'Sym_Deas')

#traversal
neighbours = Sym_Net.traverse(res,
                              direction        ='outbound',
                              item_order       ='forward',
                              min_depth        = 1,
                              max_depth        = 1,
                              vertex_uniqueness='global')

check_create_empty_collection(db, 'Sub_Sym_Deas_edges')

# neighbours['vertices']

for n in neighbours['vertices']:
  edges_of_n = Sym_Net.edge_collection('Sym_Deas_edges').edges(n)['edges']

  for ed in edges_of_n:
    outgoing_node = Sym_Net.vertex_collection('Sym_Deas').get(ed['_to'])

    if outgoing_node in neighbours['vertices']:
      try :
        db.collection('Sub_Sym_Deas_edges').insert(ed)
      except:
        pass


graph = check_create_empty_graph(db, 'Sub_Net')

if not graph.has_edge_definition('Sub_Sym_Deas_edges'):
  graph.create_edge_definition('Sub_Sym_Deas_edges', ['Sym_Deas'], ['Sym_Deas'])
