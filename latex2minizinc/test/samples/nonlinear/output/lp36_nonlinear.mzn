set of int: J = 1..M;

set of int: I = 1..N;

enum K;

array[int] of float: u;

array[int, int] of float: a;

array[int] of float: b;

array[int] of float: c;

int: N;

int: M;


array[INDEX_SET_x_1, INDEX_SET_x_2] of var int: x;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;


constraint forall(i in I, j in J)(x[i,j] >= 0);

constraint forall(j in K)(sum(i in I)(x[i,j]) >= b[j]);

constraint forall(i in I)(-sum(j in J)(x[i,j]) >= c[i]);



solve minimize sum(j in J)(u[j] * (product(i in I)(pow(a[i,j],x[i,j]) - 1)));




