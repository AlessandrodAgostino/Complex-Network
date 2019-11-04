import os
import sys
import networkx as nx
import numpy as np
path = os.path.join(os.path.dirname('__file__'),'..','data','SymptomsNet.gexf')
graph = nx.read_gexf(path)
graph.adj.items()
#%%

connectivity = dict(graph.adj.items())
#connectivity = dict(bip_graph.adj.items())


connectivity = {k[0] : list(k[1]) for k in connectivity.items()}

classes = [[],[]]
current_class = False

nodes = list(connectivity.keys())


#%%
def iteration(current_class, cur_node):        
    for node in connectivity[cur_node]:
        if (node not in classes[0]) and (node not in classes[1]):
            classes[current_class].append(node)
            iteration(not current_class, node)
#%%
sys.setrecursionlimit(10000)
iteration(current_class, nodes[0])

print(len(classes[0]), len(classes[1]), len(nodes))

a_set = set(classes[0]) 
b_set = set(classes[1]) 

print(a_set & b_set) 
#%%


for node1 in classes[0]:
    for node2 in classes[0]:
        if node1 != node2:    
            if node2 in connectivity[node1]:
                print("aiuto!")
              
#%%

path2 = os.path.join(os.path.dirname('__file__'),'..','bipartite.gexf')

bip_graph = nx.read_gexf(path2)

bip_graph




