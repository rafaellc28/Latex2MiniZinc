set of int: I = 1..m;

set of int: J = 1..n;

array[I, J] of float: c;

array[I, J] of float: a;

array[I] of float: b;

int: m;

int: n;


array[I, J] of var bool: x;


constraint forall(i in I, j in J)(assert(c[i,j] >= 0, "Assertion c[\(i),\(j)] >= 0 failed!"));

constraint forall(i in I, j in J)(assert(a[i,j] >= 0, "Assertion a[\(i),\(j)] >= 0 failed!"));

constraint forall(i in I)(assert(b[i] >= 0, "Assertion b[\(i)] >= 0 failed!"));

constraint assert(m > 0, "Assertion m > 0 failed!");

constraint assert(n > 0, "Assertion n > 0 failed!");

constraint forall(j in J)(sum(i in I)(x[i,j]) = 1);

constraint forall(i in I)(sum(j in J)(a[i,j] * x[i,j]) <= b[i]);



solve minimize sum(i in I, j in J)(c[i,j] * x[i,j]);




