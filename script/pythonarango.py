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

def saveCollection(db, name, filename):

  if db.has_collection(name):

    cursor = db.collection(name).export()
    from json import dump
    with open(filename, 'w') as file :
      dump(list(cursor.batch()), file)
  else :
    print(f'Collection {name} does not exist in this database')

def check_create_empty_collection(db, collection_name, edge=False):
  if db.has_collection(collection_name):
    db.collection(collection_name).truncate()
  else :
    db.create_collection(collection_name, edge=edge)
  return db.collection(collection_name)

def check_create_empty_graph(db, graph_name):
  if db.has_graph(graph_name):
    db.delete_graph(graph_name)
    graph = db.create_graph(name=graph_name)
  else:
    graph = db.create_graph(name=graph_name)
  return graph

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

def get_vertex(db, filter, collection_name):
  """
  filter : dictionary of conditions

  return: the document as dict
  """
  return db.collection(collection_name).find(filter).next()

def retrieve_unique_edges(list_of_paths):
  '''
  list_of_path is a very particular list.
  Result of the traversal function of python-arango, the list of path precisely.
  '''

  path_number = len(list_of_paths)
  edges = []

  for i in range(path_number):
    path = list_of_paths[i]['edges']

    for j in range(len(path)):
      if path[j] not in edges:
        edges.append(path[j])

  return edges

if __name__ == '__main__':
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
