from pyArango.connection import *
import json

# your pswd
#


def load_pass(filename):
  '''
  load password from a json file formatted like :
  {
    "username" : "root"
    "password" : "1234"
  }
  '''

  with open(filename) as f:
    doc      = json.load(f)
    password = doc['password']
  return password

conn = Connection(arangoURL='http://127.0.0.1:8529', username='root', password='')

# load your database
db = conn['_system']

# load your collections
nodes = db.collections['Sym_Deas']
edges = db.collections['Sym_Deas_edges']

def get_name(doc):
  '''
  returns nodes name

  Parameters:
    doc : Document of arango collections
  '''

  return doc['name']

def empty_collection(db, name : str):
  '''
  Check if the collection exist, and delete every document inside

  Parameters:
    db   : database object returned by a connection calls
    name : string, name of the collection to empty

  Raise:
    if the collection does not exist return Error
  '''

  if db.hasCollection(name=name):
    db.collections[name].truncate()

  else:
    raise Error('The collection does not exist on this database')


def apply_query(db, name, aql, result):
  '''
  Apply the selected query aql to collection, and store the results in a new graph/collection named result.
  if "result" already exist, it will be overwritten. If it does not exists, it will be created accordingly.

  Parameters:
    db     : database pyArango object, created by a connection.
    name   : string, name of the collection or graph to which the query is applied
    aql    : string, query to apply to "collection"
    result : string, name of the object (Graph or Query) in which the results are stored.

  Returns:

  Raise:

  '''
  pass



if db.hasCollection(name='Astenia'):

  db.collections['Astenia'].truncate() # delete every document in the collection

  aql = ("for v, e, p in 1 outbound 'Sym_Deas/N0004' Sym_Deas_edges " +
             "insert {name : v.name, dist : length(p.edges)} in Astenia")

  queryResult = db.AQLQuery(aql, rawResults=True, batchSize=1)

else :

  db.createCollection('Collection', name='Astenia')
  aql = ("for v, e, p in 1 outbound 'Sym_Deas/N0004' Sym_Deas_edges " +
             "insert {name : v.name, dist : length(p.edges)} in Astenia")

  queryResult = db.AQLQuery(aql, rawResults=True, batchSize=1)
