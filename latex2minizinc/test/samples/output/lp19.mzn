enum I;

enum J;

array[I, J] of float: C;

array[I, J] of float: A;

array[I] of float: B;


array[I, J] of var bool: x;


constraint forall(j in J)(sum(i in I)(x[i,j]) = 1);

constraint forall(i in I)(sum(j in J)(A[i,j] * x[i,j]) <= B[i]);



solve minimize sum(i in I, j in J)(C[i,j] * x[i,j]);




