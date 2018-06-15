enum ORIG;

enum DEST;

array[int, int] of float: rate;

array[int, int] of float: limit;

array[int] of float: supply;

array[int] of float: demand;


array[INDEX_SET_Trans_1, INDEX_SET_Trans_2] of var float: Trans = array2d(INDEX_SET_Trans_1, INDEX_SET_Trans_2, [0 | i in ORIG, j in DEST]);

set of int: INDEX_SET_Trans_1;

set of int: INDEX_SET_Trans_2;


constraint forall(i in ORIG)(sum(j in DEST)(Trans[i,j]) = supply[i]);

constraint forall(j in DEST)(sum(i in ORIG)(Trans[i,j]) = demand[j]);



solve minimize sum(i in ORIG, j in DEST)(rate[i,j] * pow(Trans[i,j],0.8) / (1 - Trans[i,j] / limit[i,j]));




