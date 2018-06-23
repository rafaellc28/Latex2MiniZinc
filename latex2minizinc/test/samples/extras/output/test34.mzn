enum DEST;

enum ORIG;

float: maxserve;


array[INDEX_SET_Use_1, INDEX_SET_Use_2] of var bool: Use;

set of int: INDEX_SET_Use_1 = ORIG;

set of int: INDEX_SET_Use_2 = DEST;


constraint forall(i in ORIG)(sum(j in DEST)(Use[i,j]) <= maxserve);

solve satisfy;


