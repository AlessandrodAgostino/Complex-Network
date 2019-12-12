import os

import numpy as np
import networkx as nx
from arango import ArangoClient

from near import pa_utils as pa
from time import time as now
import random as rng
# How does the computational time scale with respect on the number of node in
# the network?

# Parameters
N    = 10
P    = 0.7
SEED = 123
MAX_N = 10

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
time = []
interval = range(2, MAX_N)
for N in interval:

    graph     = nx.generators.fast_gnp_random_graph(n=N,
                                                    p=P,
                                                    seed=SEED,
                                                    directed=False)
    node_link = nx.readwrite.node_link_data(graph)
    node_link = pa.nx_to_arango(node_link, nodes_collection_name)

    timing_net = pa.export_to_arango(db, node_link,
                                     nodes_collection_name,
                                     edges_collection_name,
                                     graph_name)
    node = rng.randint(0,N-1)
    type(node)
    print(node)
    tic = now()
    first_neighbours = pa.traverse(db,node, nodes_collection_name, graph)
    toc = now()
    time.append(toc-tic)
#%%

time

pa.get_vertex(db,{"id": 0},"timing")
{'id' : starting_node}