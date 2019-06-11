enum PROD;

enum ORIG;

enum DEST;

float: minload;

array[int, int] of float: limit;


array[INDEX_SET_Trans_1, INDEX_SET_Trans_2, INDEX_SET_Trans_3] of var float: Trans;

set of int: INDEX_SET_Trans_1 = ORIG;

set of int: INDEX_SET_Trans_2 = DEST;

set of int: INDEX_SET_Trans_3 = PROD;


constraint forall(i in INDEX_SET_Trans_1, j in INDEX_SET_Trans_2, p in INDEX_SET_Trans_3)(Trans[i,j,p] >= 0);

constraint forall(i in ORIG, j in DEST where (i < to_enum(ORIG,j)))((((sum(p in PROD)(Trans[i,j,p]) = 0)) \/ (sum(p in PROD)(Trans[i,j,p]) <= limit[i,j] /\ sum(p in PROD)(Trans[i,j,p]) >= minload)) /\ 1 != 2);

solve satisfy;


