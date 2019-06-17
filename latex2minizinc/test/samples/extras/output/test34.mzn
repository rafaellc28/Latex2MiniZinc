enum DEST;

enum ORIG;

float: maxserve;


array[ORIG, DEST] of var bool: Use;


constraint forall(i in ORIG)(sum(j in DEST)(Use[i,j]) <= maxserve);

solve satisfy;


