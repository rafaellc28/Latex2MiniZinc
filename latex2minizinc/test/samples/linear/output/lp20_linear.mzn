enum PROD;

enum STAGE;

array[int] of float: profit;

array[int, int] of float: rate;

array[int] of float: avail;

array[int] of float: commit;

array[int] of float: market;

array[int] of float: avail_mean;

array[int] of float: avail_variance;


array[INDEX_SET_Make_1] of var float: Make;

set of int: INDEX_SET_Make_1;


constraint forall(p in PROD)(Make[p] <= market[p] /\ Make[p] >= commit[p]);

constraint forall(s in STAGE)(sum(p in PROD)((1/rate[p,s]) * Make[p]) <= avail[s]);



solve maximize sum(p in PROD)(profit[p] * Make[p]);



