enum ORIG;

enum DEST;

enum PROD;

array[ORIG, DEST, PROD] of float: cost;

array[ORIG, PROD] of float: supply;

array[DEST, PROD] of float: demand;

array[ORIG, DEST] of float: limit;


array[ORIG, DEST, PROD] of var float: Trans;


constraint forall(o in ORIG, d in DEST, p in PROD)(assert(cost[o,d,p] >= 0, "Assertion cost[\(o),\(d),\(p)] >= 0 failed!"));

constraint forall(o in ORIG, p in PROD)(assert(supply[o,p] >= 0, "Assertion supply[\(o),\(p)] >= 0 failed!"));

constraint forall(d in DEST, p in PROD)(assert(demand[d,p] >= 0, "Assertion demand[\(d),\(p)] >= 0 failed!"));

constraint forall(o in ORIG, d in DEST)(assert(limit[o,d] >= 0, "Assertion limit[\(o),\(d)] >= 0 failed!"));

constraint forall(o in ORIG, d in DEST, p in PROD)(Trans[o,d,p] >= 0);

constraint forall(i in ORIG, p in PROD)(sum(j in DEST)(Trans[i,j,p]) = supply[i,p]);

constraint forall(j in DEST, p in PROD)(sum(i in ORIG)(Trans[i,j,p]) = demand[j,p]);

constraint forall(i in ORIG, j in DEST)(sum(p in PROD)(Trans[i,j,p]) <= limit[i,j]);



solve minimize sum(i in ORIG, j in DEST, p in PROD)(cost[i,j,p] * Trans[i,j,p]);




