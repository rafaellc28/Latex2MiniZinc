enum ORIG;

enum DEST;

array[ORIG, DEST] of float: cost;

array[ORIG] of float: supply;

array[DEST] of float: demand;


array[ORIG, DEST] of var float: Trans;


constraint forall(o in ORIG, d in DEST)(assert(cost[o,d] >= 0, "Assertion cost[\(o),\(d)] >= 0 failed!"));

constraint forall(o in ORIG)(assert(supply[o] >= 0, "Assertion supply[\(o)] >= 0 failed!"));

constraint forall(d in DEST)(assert(demand[d] >= 0, "Assertion demand[\(d)] >= 0 failed!"));

constraint forall(o in ORIG, d in DEST)(Trans[o,d] >= 0);

constraint forall(i in ORIG)(sum(j in DEST)(Trans[i,j]) = supply[i]);

constraint forall(j in DEST)(sum(i in ORIG)(Trans[i,j]) = demand[j]);



solve minimize sum(i in ORIG, j in DEST)(cost[i,j] * Trans[i,j]);




