import os

import numpy as np
import networkx as nx
from arango import ArangoClient

from neaar import pa_utils as pa
from time import time as now
import random as rng
# How does the computational time scale with respect on the number of node in
# the network?

# Parameters
N     = 10
P     = 0.0075
SEED  = 123
MIN_N = 100
MAX_N = 8000
STEP  = 50
ITER  = 10

# Naming
nodes_collection_name = 'timing'
edges_collection_name = 'timing_edges'
graph_name = 'timing_graph'

# Access to db
host, username, password = pa.load_pass(filename='config.json')
client = ArangoClient(hosts=host)
db     = client.db('_system', username=username, password=password)

# There are infinite function for Graph Generations in Networkx, I chose the
# one with the catchier name.


filename = os.path.join(os.path.dirname('__file__'), '..' ,'data', 'timing_0_1.npy')


open(filename, 'w').close() # empty the timing file for testing DANGEROUS

times = []

for N in range(MIN_N, MAX_N, STEP):

  print(N, end='\r')

  graph = nx.generators.fast_gnp_random_graph(n=N,
                                              p=P,
                                              seed=SEED,
                                              directed=False)

  node_link = nx.readwrite.node_link_data(graph)
  node_link = pa.nx_to_arango(node_link, nodes_collection_name)

  timing_net = pa.export_to_arango(db, node_link,
                                   nodes_collection_name,
                                   edges_collection_name,
                                   graph_name)

  time = []
  for _ in range(ITER):
      # random starting node
      starting_node = rng.randint(0,N-1)

      tic = now()
      pa.traverse(db=db, starting_node=starting_node,
                   nodes_collection_name=nodes_collection_name,
                   graph_name=graph_name,
                   direction='outbound',
                   item_order='forward',
                   min_depth=0,
                   max_depth=1,
                   vertex_uniqueness='global')
      toc = now()
      time.append(toc-tic)

  times.append(time)
  np.save(filename, times)

data = np.load(filename)

import matplotlib.pyplot as plt

mean  = data.mean(axis=1)
stdev = data.std(axis=1)

stdev.shape
mean.shape

plt.plot(range(MIN_N, MAX_N, STEP), mean)
plt.fill_between(range(MIN_N, MAX_N-2, STEP), mean+stdev, mean-stdev, alpha=0.5)
plt.show()
