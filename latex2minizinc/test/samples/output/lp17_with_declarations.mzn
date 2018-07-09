set of int: I = 1..m;

set of int: J = 1..n;

array[int, int] of float: c;

int: n;

int: m;


array[INDEX_SET_x_1, INDEX_SET_x_2] of var float: x;

set of int: INDEX_SET_x_1 = I;

set of int: INDEX_SET_x_2 = J;


constraint forall(i in I, j in J)(assert(c[i,j] >= 0, "Assertion c[\(i),\(j)] >= 0 failed!"));

constraint assert(n > 0, "Assertion n > 0 failed!");

constraint assert(m > 0, "Assertion m > 0 failed!");

constraint forall(i in INDEX_SET_x_1, j in INDEX_SET_x_2)(x[i,j] >= 0);

constraint forall(i in I)(sum(j in J)(x[i,j]) <= 1);

constraint forall(j in J)(sum(i in I)(x[i,j]) = 1);



solve minimize sum(i in I, j in J)(c[i,j] * x[i,j]);




