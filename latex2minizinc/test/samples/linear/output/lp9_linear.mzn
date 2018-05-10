enum ORIG;

enum DEST;

array[int, int] of float: rate;

array[int, int] of float: Trans;

array[int, int] of float: limit;

array[int] of float: supply;

array[int] of float: demand;


constraint forall(i in ORIG)(sum(j in DEST)(Trans[i,j]) = supply[i]);

constraint forall(j in DEST)(sum(i in ORIG)(Trans[i,j]) = demand[j]);

constraint forall(i in ORIG, j in DEST)(Trans[i,j] >= 0);



solve minimize sum(i in ORIG, j in DEST)(rate[i,j] * Trans[i,j] / (1 - Trans[i,j] / limit[i,j]));




