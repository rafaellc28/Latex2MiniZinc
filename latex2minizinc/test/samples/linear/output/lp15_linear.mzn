enum P;

array[int] of float: c;

array[int] of float: a;

float: b;

array[int] of float: u;


array[INDEX_SET_X_1] of var float: X;

set of int: INDEX_SET_X_1 = P;


constraint sum(j in P)((1 / a[j]) * X[j]) <= b;

constraint forall(j in P)(X[j] <= u[j] /\ X[j] >= 0);



solve maximize sum(j in P)(c[j] * X[j]);




