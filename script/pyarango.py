from pyArango.connection import *
import json

# Some try with a Database Class

class Database():

  def __init__(name, username, password, URL='http://127.0.0.1:8529'):
    '''
    instantiate a connection with database name, and an object database self._db
    '''

    # the connection could also fail.
    conn     = Connection(URL, username=username, password=password)

    try :
      self._db = conn[name]

    except:
      raise ValueError(f'No database called {name} found')

  @property
  def name(self):
    return self._db.name

  @property
  def collections(self)
    return self._db.collections()

  def apply_query(self, name, aql, result):
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
      Error if a collection with name 'name' does not exists
    '''

    if db.hasCollection(name=name):

      if db.hasCollection(name=result):
        self._db.collections[result].truncate() # delete every document in the collection
        self._db.AQLQuery(aql, rawResults=True, batchSize=1)

      else :
        self._db.createCollection('Collection', name=result)
        queryResult = self._db.AQLQuery(aql, rawResults=True, batchSize=1)

    else :
      raise Error(f'no collection named {name} in the database {self.name}')


if __name__ == '__main__':

  # Some try with pyArango

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

  db.collections

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

    if db.hasCollection(name=name):

      if db.hasCollection(name=result):
        db.collections[result].truncate() # delete every document in the collection
        db.AQLQuery(aql, rawResults=True, batchSize=1)

      else :
        db.createCollection('Collection', name=result)
        queryResult = db.AQLQuery(aql, rawResults=True, batchSize=1)

    else :
      raise Error(f'no collection named {name} in the database {db.name}')
