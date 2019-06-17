set of int: N = 1..n;

set of int: D = [i| i in U where sum(j in N)(a[j] * x[i,j]) <= b];

set of int: U = 0..floor(pow(2,n) - 1);

array[U, N] of float: x = array2d(U, N, [floor((i div floor(pow(2,j - 1)))) mod 2 | i in U, j in N]);

int: n;

array[N] of float: a;

float: b;


array[N] of var int: alfa;

var int: beta;

set of int: INDEX_SET_U_diff_D;

array[INDEX_SET_U_diff_D] of int: U_diff_D;


constraint assert(n > 0, "Assertion n > 0 failed!");

constraint forall(j in N)(assert(a[j] >= 0, "Assertion a[\(j)] >= 0 failed!"));

constraint assert(b >= 0, "Assertion b >= 0 failed!");

constraint forall(j in N)(alfa[j] >= 0);

constraint beta >= 0;

constraint forall(i in D)(sum(j in N)(alfa[j] * x[i,j]) <= beta);

constraint forall(i in U_diff_D)(sum(j in N)(alfa[j] * x[i,j]) >= beta + 1);



solve minimize sum(j in N)(alfa[j] + beta);




