set of int: I = 1..m;

set of int: J = 1..n;

array[int, int] of float: c;

int: n;

int: m;


array[int, int] of var float: x;


constraint forall(i in I, j in J)(x[i,j] >= 0);

constraint forall(i in I)(sum(j in J)(x[i,j]) <= 1);

constraint forall(j in J)(sum(i in I)(x[i,j]) = 1);



var float: obj = sum(i in I, j in J)(c[i,j] * x[i,j]);

solve minimize obj;




