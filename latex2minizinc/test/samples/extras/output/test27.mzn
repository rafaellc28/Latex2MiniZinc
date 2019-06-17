enum PROD;

enum ORIG;

enum DEST;

array[ORIG, DEST] of float: limit;

float: minload;


array[ORIG, DEST, PROD] of var float: Trans;

array[ORIG, DEST] of var bool: Use;


constraint forall(i in ORIG, j in DEST, p in PROD)(Trans[i,j,p] >= 0);

constraint forall(i in ORIG, j in DEST)(sum(p in PROD)(Trans[i,j,p]) <= limit[i,j] * Use[i,j]);

constraint forall(i in ORIG, j in DEST)(sum(p in PROD)(Trans[i,j,p]) >= minload * Use[i,j]);

solve satisfy;


