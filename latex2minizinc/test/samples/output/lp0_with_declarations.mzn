enum I;

enum J;

array[I] of float: A;

array[I, J] of float: C;

array[J] of float: B;


array[I, J] of var int: x;


constraint forall(i in I, j in J)(x[i,j] >= 0);

constraint forall(i in I)(sum(j in J)(x[i,j]) <= A[i]);

constraint forall(j in J)(sum(i in I)(x[i,j]) >= B[j]);



var float: obj = sum(i in I, j in J)(C[i,j] * x[i,j]);

solve minimize obj;




