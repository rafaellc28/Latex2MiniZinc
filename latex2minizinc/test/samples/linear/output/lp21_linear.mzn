enum ORIG;

enum PROD;

enum DEST;

array[int, int] of float: make_cost;

array[int, int, int] of float: trans_cost;

array[int, int] of float: rate;

array[int] of float: avail;

array[int, int] of float: demand;


array[INDEX_SET_Make_1, INDEX_SET_Make_2] of var float: Make;

array[INDEX_SET_Trans_1, INDEX_SET_Trans_2, INDEX_SET_Trans_3] of var float: Trans;

set of int: INDEX_SET_Make_1 = ORIG;

set of int: INDEX_SET_Make_2 = PROD;

set of int: INDEX_SET_Trans_1 = ORIG;

set of int: INDEX_SET_Trans_2 = DEST;

set of int: INDEX_SET_Trans_3 = PROD;


constraint forall(o in ORIG, p in PROD)(assert(rate[o,p] > 0, "Assertion rate[\(o),\(p)] > 0 failed!"));

constraint forall(o in INDEX_SET_Make_1, p in INDEX_SET_Make_2)(Make[o,p] >= 0);

constraint forall(o in INDEX_SET_Trans_1, d in INDEX_SET_Trans_2, p in INDEX_SET_Trans_3)(Trans[o,d,p] >= 0);

constraint forall(i in ORIG)(sum(p in PROD)((1/rate[i,p]) * Make[i,p]) <= avail[i]);

constraint forall(i in ORIG, p in PROD)(sum(j in DEST)(Trans[i,j,p]) = Make[i,p]);

constraint forall(j in DEST, p in PROD)(sum(i in ORIG)(Trans[i,j,p]) = demand[j,p]);



solve minimize sum(i in ORIG, p in PROD)(make_cost[i,p] * Make[i,p] + sum(i in ORIG, j in DEST, p in PROD)(trans_cost[i,j,p] * Trans[i,j,p]));




