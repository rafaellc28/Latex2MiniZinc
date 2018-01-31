enum PROD;

float: avail;

array[int] of float: rate;

array[int] of float: market;


array[INDEX_SET_Make_1] of var float: Make;

set of int: INDEX_SET_Make_1;


constraint forall(p in PROD)(Make[p] >= 0);

constraint forall(p in PROD)(Make[p] <= market[p]);

constraint avail > 0 -> sum(p in PROD)((1/rate[p]) * Make[p]) <= avail;

solve satisfy;


