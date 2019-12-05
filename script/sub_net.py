from arango import ArangoClient
import json
from script.pythonarango import check_create_empty_collection, check_create_empty_graph
from script.pythonarango import load_pass, get_vertex, saveCollection

# Initialize the client for ArangoDB.
client = ArangoClient(hosts='http://127.0.0.1:8529')

# Connect to "_system" database as root user.
db = client.db('_system', username='root', password=load_pass('script/pwd.txt', isjson=False ))

Sym_Net = check_create_empty_graph(db, 'Sym_Net')

Sym_Net.create_edge_definition('Sym_Deas_edges', ['Sym_Deas'], ['Sym_Deas'])

#extracting node
res = get_vertex(db, {'name':'astenia'}, 'Sym_Deas')
#traversal
neighbours = Sym_Net.traverse(res,
                              direction        ='outbound',
                              item_order       ='forward',
                              min_depth        = 0,
                              max_depth        = 1,
                              vertex_uniqueness='global')

check_create_empty_collection(db, 'Sub_Sym_Deas_edges', edge=True)

for n in neighbours['vertices']:
  edges_of_n = Sym_Net.edge_collection('Sym_Deas_edges').edges(n, 'out')['edges']
  for ed in edges_of_n:
    outgoing_node = Sym_Net.vertex_collection('Sym_Deas').get(ed['_to'])
    if outgoing_node in neighbours['vertices']:
        db.collection('Sub_Sym_Deas_edges').insert(ed)

graph = check_create_empty_graph(db, 'Sub_Net')

if not graph.has_edge_definition('Sub_Sym_Deas_edges'):
  graph.create_edge_definition('Sub_Sym_Deas_edges', ['Sym_Deas'], ['Sym_Deas'])

filename = 'Sub_Sym_Deas_edges.json'
saveCollection(db=db, filename=filename, name='Sub_Sym_Deas_edges') # export edges collections

import networkx as nx

import json

with open(filename, 'rb') as f:
  file = json.load(f)

file

G = nx.read_edgelist(file) # yuhuuuuu


nx.readwrite.json_graph.dumps(G)
