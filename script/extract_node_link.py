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

nodes_mod = []
for line in nodes:
    diction = {}
    diction["_id"] = line["id"]
    diction["name"] = line["label"]
    nodes_mod.append(diction)

links_mod = []
for line in links:
    diction = {}
    diction["_id"] = "edges/" + line["id"]
    diction["_from"] = "commits/" + line["source"]
    diction["_to"] = "commits/" + line["target"]
    diction["vertex"] = line["source"]
    links_mod.append(diction)


nodesname = os.path.join(os.path.dirname('__file__'), '..', 'data', 'nodes.json')

linksname = os.path.join(os.path.dirname('__file__'), '..', 'data', 'links.json')

with open(nodesname, 'w', encoding='utf-8') as f:
  json.dump(obj=nodes_mod, fp=f, ensure_ascii=False, indent=2)

with open(linksname, 'w', encoding='utf-8') as f:
  json.dump(obj=links_mod, fp=f, ensure_ascii=False, indent=2)
