enum FOOD;

enum NUTR;

array[int] of float: cost;

array[int] of float: n_min;

array[int, int] of float: amt;

array[int] of float: n_max;

array[int] of float: f_min;

array[int] of float: f_max;


array[INDEX_SET_Buy_1] of var int: Buy;

set of int: INDEX_SET_Buy_1;


constraint forall(f in FOOD)(Buy[f] <= f_max[f] /\ Buy[f] >= f_min[f]);

constraint forall(i in NUTR)(sum(j in FOOD)(amt[i,j] * Buy[j]) <= n_max[i] /\ sum(j in FOOD)(amt[i,j] * Buy[j]) >= n_min[i]);



solve minimize sum(j in FOOD)(cost[j] * Buy[j]);




