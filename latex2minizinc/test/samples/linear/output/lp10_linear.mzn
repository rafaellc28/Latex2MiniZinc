enum ORIG;

enum DEST;

array[ORIG, DEST] of float: rate;

array[ORIG, DEST] of float: limit;

array[ORIG] of float: supply;

array[DEST] of float: demand;


array[ORIG, DEST] of var float: Trans;


constraint forall(o in ORIG, d in DEST)(assert(rate[o,d] >= 0, "Assertion rate[\(o),\(d)] >= 0 failed!"));

constraint forall(o in ORIG, d in DEST)(assert(limit[o,d] > 0, "Assertion limit[\(o),\(d)] > 0 failed!"));

constraint forall(o in ORIG)(assert(supply[o] >= 0, "Assertion supply[\(o)] >= 0 failed!"));

constraint forall(d in DEST)(assert(demand[d] >= 0, "Assertion demand[\(d)] >= 0 failed!"));

constraint forall(i in ORIG, j in DEST)(Trans[i,j] <= 0.9999 * limit[i,j] /\ Trans[i,j] >= 0);

constraint forall(i in ORIG)(sum(j in DEST)(Trans[i,j]) = supply[i]);

constraint forall(j in DEST)(sum(i in ORIG)(Trans[i,j]) = demand[j]);



solve minimize sum(i in ORIG, j in DEST)(rate[i,j] * Trans[i,j] / (1 - Trans[i,j] / limit[i,j]));




