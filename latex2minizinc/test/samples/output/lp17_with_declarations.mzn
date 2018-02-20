set of int: I = 1..m;

set of int: J = 1..n;

array[int, int] of float: c;

int: n;

int: m;


array[INDEX_SET_x_1, INDEX_SET_x_2] of var float: x;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;


constraint forall(i in I, j in J)(x[i,j] >= 0);

constraint forall(i in I)(sum(j in J)(x[i,j]) <= 1);

constraint forall(j in J)(sum(i in I)(x[i,j]) = 1);



solve minimize sum(i in I, j in J)(c[i,j] * x[i,j]);




