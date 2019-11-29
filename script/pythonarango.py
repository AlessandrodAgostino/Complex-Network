

from arango import ArangoClient

# Initialize the client for ArangoDB.
client = ArangoClient(hosts='http://localhost:8529')

f = open("pwd.txt","r")

pwd = f.read()
pwd = pwd[:-1]
# Connect to "_system" database as root user.
db = client.db('_system', username='root', password=pwd)
db.collections()
#db.update_permission(username='root', permission='rw', database='sym')
#db.databases()
