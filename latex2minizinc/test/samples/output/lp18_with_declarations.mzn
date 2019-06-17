set of int: I = 1..m;

set of int: J = 1..n;

array[I, J] of float: varcost;

array[I, J] of float: fixcost;

array[I] of float: supply;

array[J] of float: demand;

int: m;

int: n;


array[I, J] of var bool: y;

array[I, J] of var float: x;


constraint forall(i in I, j in J)(assert(varcost[i,j] >= 0, "Assertion varcost[\(i),\(j)] >= 0 failed!"));

constraint forall(i in I, j in J)(assert(fixcost[i,j] >= 0, "Assertion fixcost[\(i),\(j)] >= 0 failed!"));

constraint forall(i in I)(assert(supply[i] >= 0, "Assertion supply[\(i)] >= 0 failed!"));

constraint forall(j in J)(assert(demand[j] >= 0, "Assertion demand[\(j)] >= 0 failed!"));

constraint assert(m > 0, "Assertion m > 0 failed!");

constraint assert(n > 0, "Assertion n > 0 failed!");

constraint forall(i in I, j in J)(x[i,j] >= 0);

constraint forall(i in I)(sum(j in J)(x[i,j]) = supply[i]);

constraint forall(j in J)(sum(i in I)(x[i,j]) = demand[j]);

constraint forall(i in I, j in J)(x[i,j] <= min(supply[i],demand[j]) * y[i,j]);



solve minimize sum(i in I, j in J)(varcost[i,j] * x[i,j] + sum(i in I, j in J)(fixcost[i,j] * y[i,j]));




