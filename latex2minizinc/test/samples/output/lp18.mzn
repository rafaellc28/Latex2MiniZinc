enum I;

enum J;

array[I, J] of float: Varcost;

array[I, J] of float: Fixcost;

array[I] of float: Supply;

array[J] of float: Demand;


array[I, J] of var bool: y;

array[I, J] of var float: x;


constraint forall(i in I, j in J)(x[i,j] >= 0);

constraint forall(i in I)(sum(j in J)(x[i,j]) = Supply[i]);

constraint forall(j in J)(sum(i in I)(x[i,j]) = Demand[j]);

constraint forall(i in I, j in J)(x[i,j] <= min(Supply[i],Demand[j]) * y[i,j]);



solve minimize sum(i in I, j in J)(Varcost[i,j] * x[i,j] + sum(i in I, j in J)(Fixcost[i,j] * y[i,j]));




