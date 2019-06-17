enum PROD;

enum ORIG;

enum DEST;

float: minload;

array[ORIG, DEST] of float: limit;


array[ORIG, DEST, PROD] of var float: Trans;


constraint forall(i in ORIG, j in DEST, p in PROD)(Trans[i,j,p] >= 0);

constraint forall(i in ORIG, j in DEST)(sum(p in PROD)(Trans[i,j,p]) > 0 -> sum(p in PROD)(Trans[i,j,p]) <= limit[i,j] /\ sum(p in PROD)(Trans[i,j,p]) >= minload);

solve satisfy;


