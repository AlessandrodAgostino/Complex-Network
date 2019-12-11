import os

from arango import ArangoClient
import script.pa_utils as pa

#%%
# Initialize the client for ArangoDB. Connect to "_system" database as root user.
client = ArangoClient(hosts='http://127.0.0.1:8529')
db     = client.db('_system', username='root', password=pa.load_pass('script/pwd.txt', isjson=False ))

# file path
path = os.path.join(os.path.dirname('__file__'), 'data', 'SymptomsNet.gexf')

graph = pa.read_gexf(db, filename='data/SymptomsNet.gexf',
          nodes_collection_name='Sym_Deas',
          edges_collection_name='Sym_Deas_edges',
          graph_name='Sym_Net')
