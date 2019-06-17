enum P;

array[P] of float: c;

array[P] of float: a;

float: b;

array[P] of float: u;


array[P] of var float: X;


constraint sum(j in P)((1 / a[j]) * X[j]) <= b;

constraint forall(j in P)(X[j] <= u[j] /\ X[j] >= 0);



solve maximize sum(j in P)(c[j] * X[j]);




