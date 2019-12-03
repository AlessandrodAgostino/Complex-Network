from arango import ArangoClient
import json


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

if db.has_graph('Sym_Net'):
  Sym_Net = db.graph('Sym_Net')
else: Sym_Net = db.create_graph(name='Sym_Net')

if not Sym_Net.has_edge_definition('Sym_Deas_edges'):


Sym_Net.create_edge_definition('Sym_Deas_edges', ['Sym_Deas'], ['Sym_Deas'])

#extracting node
res = get_vertex({'name':'astenia'}, 'Sym_Deas')

#traversal
neighbours = Sym_Net.traverse(res,
                              direction        ='outbound',
                              item_order       ='forward',
                              min_depth        = 2,
                              max_depth        = 2,
                              vertex_uniqueness='global')

if not db.has_collection('Sub_Sym_Deas_edges'):
  db.create_collection('Sub_Sym_Deas_edges', edge = True)
else: db.collection('Sub_Sym_Deas_edges').truncate()

for n in neighbours['vertices']:
  for ed in Sym_Net.edge_collection('Sym_Deas_edges').edges(n)['edges']:
    if Sym_Net.vertex_collection('Sym_Deas').get(ed['_to']) in neighbours['vertices']:
      db.collection('Sub_Sym_Deas_edges').insert(ed)


neighbours['vertices']
