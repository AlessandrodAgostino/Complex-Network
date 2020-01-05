import os
from time import time as now
from os.path import join as pj

import numpy as np
import networkx as nx
from arango import ArangoClient
import pandas as pd
import random as rng

from neaar import pa_utils as pa

#%%
# Parameters
K     = 5 # number of path we want to search
NAME  = f'{K}_shortest_path'
P     = 0.0075
SEED  = 123
MIN_N = 200
MAX_N = 10000
STEPS = 50 # How many steps I want to collect
ITER  = 10
user  = os.getcwd().split('/')[2]

# Naming
nodes_collection_name = 'timing'
edges_collection_name = 'timing_edges'
graph_name = 'timing_graph'

# Access to db
host, username, password = pa.load_pass(filename='Complex-Network/config.json')
client = ArangoClient(hosts=host)
db     = client.db('_system', username=username, password=password)

#%%
upload_table = pd.DataFrame(columns=['Nodes Number', 'Probability', 'Upload Time (s)', 'user'])
bench_table  = pd.DataFrame(columns=['Nodes Number', 'Probability', 'Run Time (s)', 'user'])

csi   = np.divide(np.log(MAX_N / MIN_N), STEPS)
steps = np.arange(0, STEPS)

Number_Nodes = MIN_N * np.exp(csi*steps)
Number_Nodes = np.ceil(Number_Nodes).astype(int)

#%%
# Effective iteration over the desired values
for n,N in enumerate(Number_Nodes):

  print(N, end='\r')

  graph = nx.generators.fast_gnp_random_graph(n=N, p=P, directed=False)

  tic = now()
  node_link = nx.readwrite.node_link_data(graph)
  node_link = pa.nx_to_arango(node_link, nodes_collection_name)

  timing_net = pa.export_to_arango(db, node_link,
                                   nodes_collection_name,
                                   edges_collection_name,
                                   graph_name)
  toc = now()
  upload_table.loc[n] = [N, P, toc-tic, user]

  for i in range(ITER):
      # random starting node
      nodes_number = rng.sample(range(0, N-1), 2)
      node1 = '/'.join((nodes_collection_name,str(nodes_number[0])))
      node2 = '/'.join((nodes_collection_name,str(nodes_number[1])))

      tic = now()
      pa.k_shortest_path(db, node1, node2, graph_name, k=K)
      toc = now()
      bench_table.loc[n*ITER+i] = [N, P, toc-tic, user]
  bench_table.to_csv(pj('Benchmark', NAME + '.csv'), sep='\t')
  upload_table.to_csv(pj('Benchmark', NAME + '_upload.csv'), sep='\t')
  
