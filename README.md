# NEAAR

#### NEtwork Analysis in ARangodb

## Installation

To install the package, clone the repository and type on your terminal:

```shell
python setup.py install
```

Or, if you want to install in developer mode

```shell
python setup.py develop
```

## Set up

To use the package, is required to have [ArangoDB](https://www.arangodb.com/) installed.

To access the databases you'll be asked for a password: is sufficient to create a file called `config.json` on the repository with the structure:

```json
{
 "host" : "https://127.0.0.1:8529",
 "username" : "root",
 "password" : "1234"
}
```

port 8529 is the default for ArangoDB.

Now everything is set.

## Example

The full example on how to use NEAAR is reported in the file [pipeline.py](https://github.com/AlessandrodAgostino/Complex-Network/blob/master/neaar/pipeline.py) in this repository, that describe what to do in case of a multipartite graph.

```python
import os

from arango import ArangoClient # python-arango import.
import networkx as nx

from neaar import pa_utils as pa

host, username, password = pa.load_pass(filename='config.json')

# Initialize the client for ArangoDB. Connect to "_system" database as root user.
client = ArangoClient(hosts=host)
db     = client.db('_system', username=username, password=password)
```

Now a connection with the database `_system` is established.

```python
filename = 'data/multipartite.gexf'

# load a graph as multipartite and return a python-arango and a NetworkX graph
Ardb_Net, Nx_Net = pa.read_gexf(db, filename=filename, multipartite=True,
                       				nodes_collection_name='collection',
                       				edges_collection_name='edges',
                       				graph_name='multipartite')

```
Now we can run queries on the network. An example is the traversal that look for the first neighbours of a starting node:

```python
first_neighbours = pa.traverse(db=db, starting_node='2',
                                       graph_name='multipartite',
                                       direction='any',
                                       item_order='forward',
                                       min_depth=0,
                                       max_depth=1,
                                       vertex_uniqueness='global')

```

Now the dictionary `first_neighbours` contains information on nodes and paths crossed by the traversal.

It is possible to extract the subnetwork of selected nodes with the function `subgraph` of NetworkX, and save all the information

```python
# Extract subgraph
Nx_Sub_Net = Nx_Net.subgraph([vertex['label'] for vertex in astenia_first_neighbours['vertices']])

# Take back added information on Arango documents
for node in Nx_Sub_Net:
  attr = pa.get_vertex(db, {'label':node}, ["collection_0","collection_1","collection_2"])
  nx.set_node_attributes(Nx_Sub_Net, {node : attr})
```

And re-upload the subnetwork:

```python
pa.multipartite_to_arango(db,Nx_Sub_Net, "subnet","subedge","subgraph")
```

## Authors

* **Alessandro d'Agostino** [git](https://github.com/AlessandrodAgostino/)
* **Mattia Ceccarelli** [git](https://github.com/Mat092)
* **Riccardo Scheda** [git](https://github.com/riccardoscheda)
