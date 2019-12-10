"""
Some utilities based on python-arango written by us.
"""

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
  '''
  Check if a collection "collection_name" exist or not. If the former is true,
  truncate (empty) the collection, or else it will create a new one

  Parameters:
    db : Arango database, result of the function client.db of python-arango.
    collection_name : string, Name of the collection to create.
    edge : boolean, default False. If a collection of edge has to be created,
      this must be set to True.

  Returns:
    python arango collection object. Empty.

  '''

  if db.has_collection(collection_name):
    db.collection(collection_name).truncate()

  else :
    db.create_collection(collection_name, edge=edge)

  return db.collection(collection_name)

def check_create_empty_graph(db, graph_name):
  '''
  Same as for check_create_empy_collection.
  '''

  if db.has_graph(graph_name):
    db.delete_graph(graph_name)
    graph = db.create_graph(name=graph_name)

  else:
    graph = db.create_graph(name=graph_name)

  return graph

def first_neighbours(db, starting_node, nodes_collection, edges_collection, resultsname, save=False):
  '''
  That's useless now that we work with graph and traverse, but can be used as a template
  for future aql work.
  '''

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
  '''
  This function search an ArangoDB collection for a document that satisfy
  filter conditions.

  Parameters:
    db : Arango databases, result of the function client.db of python-arango.
    filter : python dictionary, list of conditions.
    collection_name : string, the collection in which the reaserch is perfomed.

  return:
    a list of document (dictionaries).
  '''

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
    Python list containing vertex and PATH crossed by the traverse.
  '''

  node = get_vertex(db, {'label' : f'{starting_node}'}, f'{nodes_collection_name}')
  Net  = db.graph(graph_name)

  result = Net.traverse(node, **kwargs)

  return result

def read_gexf(db, filename,
              nodes_collection_name='nodes',
              edges_collection_name='edges',
              graph_name='Net'):
  '''
  Creates a graph on `arangodb` from a gexf file. Requires `networkx` to be installed.

  Read the graph with the function `read_gexf` of `networkx` and generates a json formatted with
  `node_link_data`, containing

  Parameters:
    db       : Arango databases, result of the function client.db of python-arango
    filename : string, name of the .gexf file to be read
    nodes_collection_name : string, default "nodes". Name of the collection in which nodes
                            informations are stored. Be carefull, if the collection already exists,
                            it will be truncated.
    edges_collection_name : string, default "edges". Name of the collection in which edges
                            informations are stored. Be carefull, if the collection already exists,
                            it will be truncated.
    graph_name : string, default "Net". Name of the graph created from the collections.
                 Be carefull, if the graph already exists, it will be overwritten.

  Returns:
    graph object of python-arango
  '''

  # Is it correct to perform the import here? is it better to do it at script's top?
  from networkx import read_gexf as rgexf
  from networkx.readwrite import node_link_data
  from math import log, ceil

  graph      = rgexf(filename)
  nodes_list = list(graph.nodes())   # needed for link document creation
  graph      = node_link_data(graph) # override graph, is not usefull anymore here

  # Number of digit needed for counting the nodes:
  format_len_node = ceil(log(len(graph['nodes']),10))

  # Number of digit needed for counting the links:
  format_len_link = ceil(log(len(graph['links']),10))

  # Adding required '_key' attribute for Arango managing
  for n,node in enumerate(graph['nodes']):
    node['_key'] = f'N{n:{0}{format_len_node}}'
    
  # Adding required '_key', '_to', '_from' attribute for Arango managing
  for n,link in enumerate(graph['links']):
    link['_key']  = 'E{}'.format(str(n).zfill(format_len_link))
    link['_to']   = '{}/N{}'.format(nodes_collection_name,str(nodes_list.index(link['target'])).zfill(format_len_node))
    link['_from'] = '{}/N{}'.format(nodes_collection_name,str(nodes_list.index(link['source'])).zfill(format_len_node))

  # Create nodes collection and insert all the nodes in the net
  Sym_Deas = check_create_empty_collection(db=db, collection_name=nodes_collection_name, edge=False)
  Sym_Deas.insert_many(graph['nodes'])

  # Create links collection and inser all the edges in the net
  Sym_Deas_edges = check_create_empty_collection(db=db, collection_name=edges_collection_name, edge=True)
  Sym_Deas_edges.insert_many(graph['links'])

  # Directly create the graph and add egde collection
  Net = check_create_empty_graph(db=db, graph_name=graph_name)
  Net.create_edge_definition(edges_collection_name, [nodes_collection_name], [nodes_collection_name])

  return Net
