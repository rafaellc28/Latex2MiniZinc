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

set of int: INDEX_SET_x_1 = I;

set of int: INDEX_SET_x_2 = J;


constraint forall(j in J)(assert(u[j] >= 0, "Assertion u[\(j)] >= 0 failed!"));

constraint forall(i in I, j in J)(assert(a[i,j] <= 1 /\ a[i,j] >= 0, "Assertion a[\(i),\(j)] <= 1 /\\ a[\(i),\(j)] >= 0 failed!"));

constraint forall(j in K)(assert(b[j] >= 0, "Assertion b[\(j)] >= 0 failed!"));

constraint forall(i in I)(assert(c[i] <= 0, "Assertion c[\(i)] <= 0 failed!"));

constraint assert(N > 0, "Assertion N > 0 failed!");

constraint assert(M > 0, "Assertion M > 0 failed!");

constraint forall(i in INDEX_SET_x_1, j in INDEX_SET_x_2)(x[i,j] >= 0);

constraint forall(j in K)(sum(i in I)(x[i,j]) >= b[j]);

constraint forall(i in I)(-sum(j in J)(x[i,j]) >= c[i]);



solve minimize sum(j in J)(u[j] * (product(i in I)(pow(a[i,j],x[i,j]) - 1)));




