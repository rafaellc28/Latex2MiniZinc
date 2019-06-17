set of int: J = 1..M;

set of int: I = 1..N;

array[J] of float: y;

array[J] of float: t = array1d(J, [10 * (j - 1) | j in J]);

int: N;

int: M;


array[I] of var float: x;


constraint assert(N > 0, "Assertion N > 0 failed!");

constraint assert(M > 0, "Assertion M > 0 failed!");

constraint forall(i in I)(x[i] <= 10);





solve minimize sum(j in J)(pow((y[j] - (x[1] + x[2] * exp(-t[j] * x[4]) + x[3] * exp(-t[j] * x[5]))),2));




