set of int: I = 1..m;

set of int: J = 1..n;

array[int, int] of float: c;

array[int, int] of float: a;

array[int] of float: b;

int: m;

int: n;


array[INDEX_SET_x_1, INDEX_SET_x_2] of var bool: x;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;


constraint forall(j in J)(sum(i in I)(x[i,j]) = 1);

constraint forall(i in I)(sum(j in J)(a[i,j] * x[i,j]) <= b[i]);



var float: obj = sum(i in I, j in J)(c[i,j] * x[i,j]);

solve minimize obj;




