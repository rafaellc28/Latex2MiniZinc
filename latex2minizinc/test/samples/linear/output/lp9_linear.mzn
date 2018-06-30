enum ORIG;

enum DEST;

array[int, int] of float: rate;

array[int, int] of float: limit;

array[int] of float: supply;

array[int] of float: demand;


array[INDEX_SET_Trans_1, INDEX_SET_Trans_2] of var float: Trans;

set of int: INDEX_SET_Trans_1 = ORIG;

set of int: INDEX_SET_Trans_2 = DEST;


constraint forall(o in ORIG, d in DEST)(assert(rate[o,d] >= 0, "Assertion rate[\(o),\(d)] >= 0 failed!"));

constraint forall(o in ORIG)(assert(supply[o] >= 0, "Assertion supply[\(o)] >= 0 failed!"));

constraint forall(d in DEST)(assert(demand[d] >= 0, "Assertion demand[\(d)] >= 0 failed!"));

constraint forall(i in INDEX_SET_Trans_1, j in INDEX_SET_Trans_2)(Trans[i,j] >= 0);

constraint forall(i in ORIG)(sum(j in DEST)(Trans[i,j]) = supply[i]);

constraint forall(j in DEST)(sum(i in ORIG)(Trans[i,j]) = demand[j]);



solve minimize sum(i in ORIG, j in DEST)(rate[i,j] * Trans[i,j] / (1 - Trans[i,j] / limit[i,j]));




