set of int: I = 1..m;

set of int: J = 1..n;

array[int, int] of float: varcost;

array[int, int] of float: fixcost;

array[int] of float: supply;

array[int] of float: demand;

int: m;

int: n;


array[INDEX_SET_y_1, INDEX_SET_y_2] of var bool: y;

array[INDEX_SET_x_1, INDEX_SET_x_2] of var float: x;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;

set of int: INDEX_SET_y_1;

set of int: INDEX_SET_y_2;


constraint forall(i in I, j in J)(x[i,j] >= 0);

constraint forall(i in I)(sum(j in J)(x[i,j]) = supply[i]);

constraint forall(j in J)(sum(i in I)(x[i,j]) = demand[j]);

constraint forall(i in I, j in J)(x[i,j] <= min(supply[i],demand[j]) * y[i,j]);



var float: obj = sum(i in I, j in J)(varcost[i,j] * x[i,j] + sum(i in I, j in J)(fixcost[i,j] * y[i,j]));

solve minimize obj;




