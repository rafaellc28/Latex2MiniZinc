enum I;

enum J;

array[int, int] of float: Varcost;

array[int, int] of float: Fixcost;

array[int] of float: Supply;

array[int] of float: Demand;


array[int, int] of var bool: y;

array[int, int] of var float: x;


constraint forall(i in I, j in J)(x[i,j] >= 0);

constraint forall(i in I)(sum(j in J)(x[i,j]) = Supply[i]);

constraint forall(j in J)(sum(i in I)(x[i,j]) = Demand[j]);

constraint forall(i in I, j in J)(x[i,j] <= min(Supply[i],Demand[j]) * y[i,j]);



var float: obj = sum(i in I, j in J)(Varcost[i,j] * x[i,j] + sum(i in I, j in J)(Fixcost[i,j] * y[i,j]));

solve minimize obj;




