enum PROD;

enum ORIG;

enum DEST;

float: minload;

array[int, int] of float: limit;


array[INDEX_SET_Trans_1, INDEX_SET_Trans_2, INDEX_SET_Trans_3] of var float: Trans;

set of int: INDEX_SET_Trans_1;

set of int: INDEX_SET_Trans_2;

set of int: INDEX_SET_Trans_3;


constraint forall(i in ORIG, j in DEST, p in PROD)(Trans[i,j,p] >= 0);

constraint forall(i in ORIG, j in DEST)(sum(p in PROD)(Trans[i,j,p]) = 0 \/ sum(p in PROD)(Trans[i,j,p]) <= limit[i,j] /\ sum(p in PROD)(Trans[i,j,p]) >= minload);

solve satisfy;


