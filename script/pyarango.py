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

conn = Connection(arangoURL='http://127.0.0.1:8529', username='root', password='your_arangoDB_pass')

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


if db.hasCollection(name='Astenia'):
  # not complete
  ql = ("for v, e, p in 1 outbound 'Sym_Deas/N0004' Sym_Deas_edges " +
             "insert {name : v.name, dist : length(p.edges)} in Astenia")

  queryResult = db.AQLQuery(aql, rawResults=True, batchSize=1)
  # it works!
else :
  astenia = db.createCollection('Collection', name='Astenia')
  ql = ("for v, e, p in 1 outbound 'Sym_Deas/N0004' Sym_Deas_edges " +
             "insert {name : v.name, dist : length(p.edges)} in Astenia")

  queryResult = db.AQLQuery(aql, rawResults=True, batchSize=1)
  # it works!
