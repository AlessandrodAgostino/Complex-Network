var graph_module = require("@arangodb/general-graph");
var edgeDefinitions = [ { collection: "Sym_Deas_edges", "from": [ "Sym_Deas" ], "to" : [ "Sym_Deas" ] } ];
//graph = graph_module._create("Sym_Deas_Net", edgeDefinitions);

var res = db._query(`FOR doc in Sym_Deas RETURN doc.name`);
while(res.hasNext()){
  var doc = res.next()
  print(doc)
}
res = Array.from(res)
print(res.length)



graph._neighbors(graph.Sym_Deas[0])
