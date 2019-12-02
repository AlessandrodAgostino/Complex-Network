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


if __name__ == '__main__':

  from arango import ArangoClient
  import json

  # Initialize the client for ArangoDB.
  client = ArangoClient(hosts='http://127.0.0.1:8529')

  # Connect to "_system" database as root user.
  db = client.db('_system', username='root', password=load_pass('pwd.txt', isjson=False ))

  first_neighbours(db=db,
                   starting_node='astenia',
                   nodes_collection='Sym_Deas',
                   edges_collection='Sym_Deas_edges',
                   resultsname='Astenia',
                   save=False)



  # query = 'FOR v,e,p IN 1..1 ANY "Sym_Deas/N0010" edges return v'
  #
  # file = db.aql.execute(query)
  # res = file.fetch()
  #
  #
#  db.delete_graph('astenia')
