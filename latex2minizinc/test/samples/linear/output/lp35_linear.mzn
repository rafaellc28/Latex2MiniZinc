enum ORIG;

enum DEST;

enum PROD;

array[int, int, int] of float: cost;

array[int, int] of float: supply;

array[int, int] of float: demand;

array[int, int] of float: limit;


array[INDEX_SET_Trans_1, INDEX_SET_Trans_2, INDEX_SET_Trans_3] of var float: Trans;

set of int: INDEX_SET_Trans_1 = ORIG;

set of int: INDEX_SET_Trans_2 = DEST;

set of int: INDEX_SET_Trans_3 = PROD;


constraint forall(o in INDEX_SET_Trans_1, d in INDEX_SET_Trans_2, p in INDEX_SET_Trans_3)(Trans[o,d,p] >= 0);

constraint forall(i in ORIG, p in PROD)(sum(j in DEST)(Trans[i,j,p]) = supply[i,p]);

constraint forall(j in DEST, p in PROD)(sum(i in ORIG)(Trans[i,j,p]) = demand[j,p]);

constraint forall(i in ORIG, j in DEST)(sum(p in PROD)(Trans[i,j,p]) <= limit[i,j]);



solve minimize sum(i in ORIG, j in DEST, p in PROD)(cost[i,j,p] * Trans[i,j,p]);




