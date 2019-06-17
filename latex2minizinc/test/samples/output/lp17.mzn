enum I;

enum J;

array[I, J] of float: C;


array[I, J] of var float: x;


constraint forall(i in I, j in J)(x[i,j] >= 0);

constraint forall(i in I)(sum(j in J)(x[i,j]) <= 1);

constraint forall(j in J)(sum(i in I)(x[i,j]) = 1);



solve minimize sum(i in I, j in J)(C[i,j] * x[i,j]);




