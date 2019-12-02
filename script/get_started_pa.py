from arango import ArangoClient

def load_pass(filename, isjson=True):
    with open(filename) as f:
      password = f.read()
      password = password[:-1]
    return password

pwd = load_pass('pwd.txt')


# Initialize the client for ArangoDB.
client = ArangoClient(hosts='http://localhost:8529')

# Connect to "_system" database as root user.
sys_db = client.db('_system', username='root', password=pwd)

# Create a new database named "test".
sys_db.create_database('test')

# Connect to "test" database as root user.
db = client.db('test', username='root', password=pwd)

# Create a new collection named "students".
students = db.create_collection('students')

# Add a hash index to the collection.
students.add_hash_index(fields=['name'], unique=True)

# Insert new documents into the collection.
students.insert({'name': 'jane', 'age': 39})
students.insert({'name': 'josh', 'age': 18})
students.insert({'name': 'judy', 'age': 21})

# Execute an AQL query and iterate through the result cursor.
cursor = db.aql.execute('FOR doc IN students RETURN doc')
student_names = [document['name'] for document in cursor]
