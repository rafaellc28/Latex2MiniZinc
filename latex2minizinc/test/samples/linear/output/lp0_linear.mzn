enum INPUT;

enum OUTPUT;

array[int] of float: cost;

array[int] of float: out_min;

array[int, int] of float: io;

array[int] of float: out_max;

array[int] of float: in_min;

array[int] of float: in_max;


array[INDEX_SET_X_1] of var float: X;

set of int: INDEX_SET_X_1;


constraint forall(j in INPUT)(X[j] <= in_max[j] /\ X[j] >= in_min[j]);

constraint forall(i in OUTPUT)(sum(j in INPUT)(io[i,j] * X[j]) <= out_max[i] /\ sum(j in INPUT)(io[i,j] * X[j]) >= out_min[i]);



solve minimize sum(j in INPUT)(cost[j] * X[j]);




