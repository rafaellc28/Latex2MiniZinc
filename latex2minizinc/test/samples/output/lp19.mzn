enum I;

enum J;

array[int, int] of float: C;

array[int, int] of float: A;

array[int] of float: B;


array[int, int] of var bool: x;


constraint forall(j in J)(sum(i in I)(x[i,j]) = 1);

constraint forall(i in I)(sum(j in J)(A[i,j] * x[i,j]) <= B[i]);



var float: obj = sum(i in I, j in J)(C[i,j] * x[i,j]);

solve minimize obj;




