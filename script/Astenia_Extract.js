const fs = require('fs');
to 
var res = db._query(`FOR doc in Sym_Deas RETURN doc`);
while(res.hasNext()){
  var doc = res.next()
  neighbours.push(db._query(`
    for v, e, p in 1 outbound '${doc['_id']}' Sym_Deas_edges
      return {name : v.name, dist: length(p.edges), origin_id:'${doc['_id']}', origin_name:'${doc['name']}'}`))
}
print(neighbours[3])
// let data = JSON.stringify(neighbours);
// fs.writeFileSync('neighbours.json', data);
