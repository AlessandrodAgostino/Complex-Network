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

def first_neighbours(db, collection, node, name, save=False):
  
  bind_vars={
      '@collection' : collection,
      'node'        : node,
      '@result'     : name
      }
  
  aql = 'FOR v,e,p IN 1..1 ANY @node @@collection'

  if save:
  
    aql += ' RETURN doc'
    res  = db.aql.execute(aql, bind_vars=bind_vars)
    
    with open(name, 'w') as file:
      json.dump(res, file)
    
  else : 

   
    
    aql += ' INSERT v IN @@result'
    db.aql.execute(aql, bind_vars=bind_vars)
    
  
if __name__ == '__main__':
  
  from arango import ArangoClient
  import json
  
  # Initialize the client for ArangoDB.
  client = ArangoClient(hosts='http://127.0.0.1:8529')
  
  # Connect to "_system" database as root user.
  db = client.db('_system', username='root', password=load_pass('pwd.txt', isjson=False ))
  
  query = 'FOR v IN 1..1 ANY FILTER v.name == "Astenia" "Sym_Deas"  edges'
    
  db.aql.execute(query)
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

