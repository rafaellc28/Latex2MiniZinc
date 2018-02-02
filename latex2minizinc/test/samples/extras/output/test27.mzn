enum PROD;

enum ORIG;

enum DEST;

array[int, int] of float: limit;

float: minload;


array[INDEX_SET_Trans_1, INDEX_SET_Trans_2, INDEX_SET_Trans_3] of var float: Trans;

array[INDEX_SET_Use_1, INDEX_SET_Use_2] of var bool: Use;

set of int: INDEX_SET_Trans_1;

set of int: INDEX_SET_Trans_2;

set of int: INDEX_SET_Trans_3;

set of int: INDEX_SET_Use_1;

set of int: INDEX_SET_Use_2;


constraint forall(i in ORIG, j in DEST, p in PROD)(Trans[i,j,p] >= 0);

constraint forall(i in ORIG, j in DEST)(sum(p in PROD)(Trans[i,j,p]) <= limit[i,j] * Use[i,j]);

constraint forall(i in ORIG, j in DEST)(sum(p in PROD)(Trans[i,j,p]) >= minload * Use[i,j]);

solve satisfy;


