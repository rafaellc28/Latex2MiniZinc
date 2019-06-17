enum N;

set of int: D;

set of int: U;

array[U, N] of float: X;


array[N] of var int: alfa;

var int: beta;

set of int: INDEX_SET_U_diff_D;

array[INDEX_SET_U_diff_D] of int: U_diff_D;


constraint forall(j in N)(alfa[j] >= 0);

constraint beta >= 0;

constraint forall(i in D)(sum(j in N)(alfa[j] * X[i,j]) <= beta);

constraint forall(i in U_diff_D)(sum(j in N)(alfa[j] * X[i,j]) >= beta + 1);

constraint forall(i in U, j in N)(X[i,j] >= 0);



solve minimize sum(j in N)(alfa[j] + beta);




