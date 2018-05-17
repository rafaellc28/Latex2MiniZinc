enum PROD;

array[int] of float: profit;

array[int] of float: rate;

float: avail;

array[int] of float: market;


array[INDEX_SET_Make_1] of var float: Make;

set of int: INDEX_SET_Make_1;


constraint forall(p in PROD)(Make[p] <= market[p] /\ Make[p] >= 0);

constraint sum(p in PROD)((1/rate[p]) * Make[p]) <= avail;



solve maximize sum(p in PROD)(profit[p] * Make[p]);




