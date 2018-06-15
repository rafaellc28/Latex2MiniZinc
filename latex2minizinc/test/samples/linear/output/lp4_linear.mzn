enum FOOD;

set of int: MINREQ;

set of int: MAXREQ;

set of int: NUTR = MINREQ union MAXREQ;

array[int] of float: cost;

array[int, int] of float: amt;

array[int] of float: n_min;

array[int] of float: n_max;

array[int] of float: f_min;

array[int] of float: f_max;


array[INDEX_SET_Buy_1] of var float: Buy = array1d(INDEX_SET_Buy_1, [f_min[f] | f in FOOD]);

set of int: INDEX_SET_Buy_1;


constraint forall(i in MINREQ)(sum(j in FOOD)(amt[i,j] * Buy[j]) >= n_min[i]);

constraint forall(i in MAXREQ)(sum(j in FOOD)(amt[i,j] * Buy[j]) <= n_max[i]);



solve minimize sum(j in FOOD)(cost[j] * Buy[j]);




