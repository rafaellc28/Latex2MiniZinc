enum ORIG;

enum DEST;

enum PROD;

array[int, int, int] of float: vcost;

array[int, int] of float: fcost;

array[int, int] of float: supply;

array[int, int] of float: demand;

array[int, int] of float: limit;

float: minload;

int: maxserve;


array[INDEX_SET_Trans_1, INDEX_SET_Trans_2, INDEX_SET_Trans_3] of var float: Trans;

array[INDEX_SET_Use_1, INDEX_SET_Use_2] of var bool: Use;

set of int: INDEX_SET_Trans_1 = ORIG;

set of int: INDEX_SET_Trans_2 = DEST;

set of int: INDEX_SET_Trans_3 = PROD;

set of int: INDEX_SET_Use_1 = ORIG;

set of int: INDEX_SET_Use_2 = DEST;


constraint forall(o in ORIG, d in DEST, p in PROD)(assert(vcost[o,d,p] >= 0, "Assertion vcost[\(o),\(d),\(p)] >= 0 failed!"));

constraint forall(o in ORIG, d in DEST)(assert(fcost[o,d] >= 0, "Assertion fcost[\(o),\(d)] >= 0 failed!"));

constraint forall(o in ORIG, p in PROD)(assert(supply[o,p] >= 0, "Assertion supply[\(o),\(p)] >= 0 failed!"));

constraint forall(d in DEST, p in PROD)(assert(demand[d,p] >= 0, "Assertion demand[\(d),\(p)] >= 0 failed!"));

constraint forall(o in ORIG, d in DEST)(assert(limit[o,d] >= 0, "Assertion limit[\(o),\(d)] >= 0 failed!"));

constraint assert(minload >= 0, "Assertion minload >= 0 failed!");

constraint forall(o in INDEX_SET_Trans_1, d in INDEX_SET_Trans_2, p in INDEX_SET_Trans_3)(Trans[o,d,p] >= 0);

constraint forall(i in ORIG, p in PROD)(sum(j in DEST)(Trans[i,j,p]) = supply[i,p]);

constraint forall(j in DEST, p in PROD)(sum(i in ORIG)(Trans[i,j,p]) = demand[j,p]);

constraint forall(i in ORIG, j in DEST)(sum(p in PROD)(Trans[i,j,p]) <= limit[i,j] * Use[i,j]);

constraint forall(i in ORIG, j in DEST)(sum(p in PROD)(Trans[i,j,p]) >= minload * Use[i,j]);

constraint forall(i in ORIG)(sum(j in DEST)(Use[i,j]) <= maxserve);



solve minimize sum(i in ORIG, j in DEST, p in PROD)(vcost[i,j,p] * Trans[i,j,p] + sum(i in ORIG, j in DEST)(fcost[i,j] * Use[i,j]));




