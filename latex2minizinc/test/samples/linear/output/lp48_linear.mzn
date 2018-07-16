enum ORIG;

enum DEST;

float: lambda = 0.85;

array[int, int] of float: cost;

array[int] of float: supply;

array[int] of float: demand;


array[INDEX_SET_Trans_1, INDEX_SET_Trans_2] of var float: Trans;

set of int: INDEX_SET_Trans_1 = ORIG;

set of int: INDEX_SET_Trans_2 = DEST;


constraint forall(o in ORIG, d in DEST)(assert(cost[o,d] >= 0, "Assertion cost[\(o),\(d)] >= 0 failed!"));

constraint forall(o in ORIG)(assert(supply[o] >= 0, "Assertion supply[\(o)] >= 0 failed!"));

constraint forall(d in DEST)(assert(demand[d] >= 0, "Assertion demand[\(d)] >= 0 failed!"));

constraint forall(o in INDEX_SET_Trans_1, d in INDEX_SET_Trans_2)(Trans[o,d] >= 0);

constraint forall(i in ORIG)(sum(j in DEST)(Trans[i,j]) = supply[i]);

constraint forall(j in DEST)(sum(i in ORIG)(Trans[i,j]) = demand[j]);



solve minimize lambda * sum(i in ORIG, j in DEST)(cost[i,j] * Trans[i,j] + (1 - lambda) * sum(i in ORIG, j in DEST)(cost[i,j] * Trans[i,j]));




