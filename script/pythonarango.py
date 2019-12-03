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

def saveCollection(name, filename, database):

  if db.has_collection(name):

    cursor = db.collection(name).export()
    with open(filename, 'w') as file :
      json.dump(cursor.fetch(), file)

  else :
    print(f'Collection {name} does not exist in this database')

def check_create_empty_collection(db, collection_name):

  if db.has_collection(collection_name):

    db.collection(collection_name).truncate()

  else :
    db.create_collection(collection_name)

def first_neighbours(db, starting_node, nodes_collection, edges_collection, resultsname, save=False):

  bind_vars={
      'starting_node' : starting_node,
      '@edges'        : edges_collection,
      '@nodes'        : nodes_collection,
      '@result'       : resultsname,
      '@result_edges' : resultsname + '_edges',
      }

  aql = 'FOR c IN @@nodes filter c.name == @starting_node FOR v,e IN 1..1 ANY c._id @@edges'

  if save:

    aql += ' RETURN v'
    res  = db.aql.execute(aql, bind_vars=bind_vars)

    with open(resultsname, 'w') as file:
      json.dump(res, file)

  else :

    results_edges = resultsname + '_edges'

    check_create_empty_collection(db, resultsname)   # create or truncate the collection resultname
    check_create_empty_collection(db, results_edges) # create or truncate the collection resultname_edges

    aql += ' INSERT v IN @@result INSERT e in @@result_edges'
    db.aql.execute(aql, bind_vars=bind_vars)

def get_vertex(filter, collection_name):
  """
  filter : dictionary of conditions

  return: the document as dict
  """
  return db.collection(collection_name).find(filter).batch()[0]


def main():
  from arango import ArangoClient
  import json

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



if __name__ == '__main__':
  main()
