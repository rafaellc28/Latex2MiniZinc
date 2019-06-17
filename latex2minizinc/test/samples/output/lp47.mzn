enum I;

array[I] of float: A;

float: BigM;


array[I, I] of var bool: y;

array[I] of var float: t;


constraint forall(i in I, j in I where i != j)(A[i] <= A[j] + BigM * y[i,j]);

constraint forall(i in I, j in I where i != j)(A[j] <= A[i] + BigM * (1 - y[i,j]));

constraint forall(i in I, j in I where i != j)(y[i,j] + y[j,i] = 1);

constraint forall(i in I)(t[i] = 1 + sum(j in I where i != j)(y[i,j]));

solve satisfy;


