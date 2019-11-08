import json
import os

filename = os.path.join(os.path.dirname('__file__'), '..', 'data', 'Symptoms.json')

with open(filename) as file:
  graph = json.load(file)

nodes = graph['nodes']
links  = graph['links']

dictionary = {'source' : '_from',
              'target' : '_to',
              "'"      : '"',
}

nodes

nodes_mod = {}
for line in nodes:
  nodes_mod['_id'] = line['id']

nodesname = os.path.join(os.path.dirname('__file__'), '..', 'data', 'nodes.json')
linksname = os.path.join(os.path.dirname('__file__'), '..', 'data', 'links.json')

with open(nodesname, 'w', encoding='utf-8') as f:
  json.dump(obj=nodes, fp=f, ensure_ascii=False, indent=2)

with open(linksname, 'w', encoding='utf-8') as f:
  json.dump(obj=links, fp=f, ensure_ascii=False, indent=2)
