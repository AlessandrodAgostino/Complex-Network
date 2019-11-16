// try {
//   db.Astenia.drop()
// } catch(error) {}
// db._create('Astenia')
// db._query(`for v, e, p in 1 outbound 'Sym_Deas/N0004' Sym_Deas_edges
//     insert {name : v.name, dist: length(p.edges)} in Astenia`)
// Astenia = db._query(`FOR c IN Astenia     RETURN c`)
// let soMany = 10
// print(`This is ${soMany} times easier!`)


neighbours = []
var res = db._query(`FOR doc in Sym_Deas RETURN doc`);
while(res.hasNext()){
  var doc = res.next()
  neighbours.push(db._query(`
    for v, e, p in 1 outbound '${doc['_id']}' Sym_Deas_edges
      return {name : v.name, dist: length(p.edges), origin_id:'${doc['_id']}', origin_name:'${doc['name']}'}`))
}

print(neighbours[1])
