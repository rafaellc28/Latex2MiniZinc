enum ORIG;

enum PROD;

enum DEST;

array[ORIG, PROD] of float: make_cost;

array[ORIG, DEST, PROD] of float: trans_cost;

array[ORIG, PROD] of float: rate;

array[ORIG] of float: avail;

array[DEST, PROD] of float: demand;


array[ORIG, PROD] of var float: Make;

array[ORIG, DEST, PROD] of var float: Trans;


constraint forall(o in ORIG, p in PROD)(assert(rate[o,p] > 0, "Assertion rate[\(o),\(p)] > 0 failed!"));

constraint forall(o in ORIG, p in PROD)(Make[o,p] >= 0);

constraint forall(o in ORIG, d in DEST, p in PROD)(Trans[o,d,p] >= 0);

constraint forall(i in ORIG)(sum(p in PROD)((1/rate[i,p]) * Make[i,p]) <= avail[i]);

constraint forall(i in ORIG, p in PROD)(sum(j in DEST)(Trans[i,j,p]) = Make[i,p]);

constraint forall(j in DEST, p in PROD)(sum(i in ORIG)(Trans[i,j,p]) = demand[j,p]);



solve minimize sum(i in ORIG, p in PROD)(make_cost[i,p] * Make[i,p] + sum(i in ORIG, j in DEST, p in PROD)(trans_cost[i,j,p] * Trans[i,j,p]));




