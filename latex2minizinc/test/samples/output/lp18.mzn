enum I;

enum J;

array[int, int] of float: Varcost;

array[int, int] of float: Fixcost;

array[int] of float: Supply;

array[int] of float: Demand;


array[INDEX_SET_y_1, INDEX_SET_y_2] of var bool: y;

array[INDEX_SET_x_1, INDEX_SET_x_2] of var float: x;

set of int: INDEX_SET_x_1 = I;

set of int: INDEX_SET_x_2 = J;

set of int: INDEX_SET_y_1 = I;

set of int: INDEX_SET_y_2 = J;


constraint forall(i in INDEX_SET_x_1, j in INDEX_SET_x_2)(x[i,j] >= 0);

constraint forall(i in I)(sum(j in J)(x[i,j]) = Supply[i]);

constraint forall(j in J)(sum(i in I)(x[i,j]) = Demand[j]);

constraint forall(i in I, j in J)(x[i,j] <= min(Supply[i],Demand[j]) * y[i,j]);



solve minimize sum(i in I, j in J)(Varcost[i,j] * x[i,j] + sum(i in I, j in J)(Fixcost[i,j] * y[i,j]));




