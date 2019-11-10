#Ale 10/11/2019
import os
import json
import math
import networkx as nx
import pylab as plt
import numpy as np
path = os.path.join(os.path.dirname('__file__'), '..' ,'data', 'SymptomsNet.gexf')
graph = nx.read_gexf(path)
#%%
nodes = list(graph.nodes())
length = round(math.log(len(nodes),10)) + 1

nodes_dict = [{"name": name, "_key": 'N{}'.format(str(n).zfill(length))} for n,name in enumerate(nodes)]


"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
This JSON has to be imported is a Collection named "Sym_Deas"
"""
with open('/home/alessandro/Dropbox/Chimera/Sym_nodes_Ale.json', 'w') as fout:
    json.dump(nodes_dict , fout, ensure_ascii=False)

#%%
edges = list(graph.edges())
edges_dict = []
for edge in edges:
    edges_dict.append({"_from" : "Sym_Deas/N{}".format(str(nodes.index(edge[0])).zfill(length)),
                       "_to" : "Sym_Deas/N{}".format(str(nodes.index(edge[1])).zfill(length))})

with open('/home/alessandro/Dropbox/Chimera/Sym_edges_Ale.json', 'w') as fout:
    json.dump(edges_dict , fout, ensure_ascii=False)
