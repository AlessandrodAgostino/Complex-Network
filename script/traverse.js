var traversal = require("org/arangodb/graph/traversal");

var knownFilter = function(config, vertex, path) {
  if (config.known[vertex._key] !== undefined) {
    return "prune";
  }
  return "";
};

var sumVisitor = function(config, result, vertex, path) {
  if (config.known[vertex._key] !== undefined) {
    result.sum += config.known[vertex._key];
  } else {
    config.known[vertex._key] = result.sum;
  }
  result.sum += 1;
  return;
};

var config = {
  datasource: traversal.collectionDatasourceFactory(db.e), // e is my edge collection
  strategy: "depthfirst",
  order: "preorder",
  filter: knownFilter,
  expander: traversal.outboundExpander,
  visitor: sumVisitor,
  known: {}
};

var traverser = new traversal.Traverser(config);
var cursor = db.v.all(); // v is my vertex collection

while(cursor.hasNext()) {
  var node = cursor.next();
  traverser.traverse({sum: 0}, node);
}

config.known; // Returns the result of type name: counter. In arangosh this will print out complete result
