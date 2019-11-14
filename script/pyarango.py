from pyArango.connection import *

##your pswd

#load your database
db = con["symptoms"]

#load your collection
nodes = db.collections["nodes"]
edges = db.collections["edges"]

#node1 è un singolo documento della collezione nodes, quindi se ho capito bene ogni nodo è un documento
#della collezione nodes
node1 = nodes["N0000"]

#accede al nome del nodo
def report(document):
    print("malattia : %s" %document["name"])

report(node1)
# aql = "FOR x IN nodes RETURN x._key"
# queryResult = db.AQLQuery(aql, rawResults=True, batchSize=0)
# for key in queryResult:
#     print(key)
