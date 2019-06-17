enum J;

enum I;

array[I] of float: W;

float: C;


array[J] of var bool: used;

array[I, J] of var bool: x;


constraint forall(i in I)(sum(j in J)(x[i,j]) = 1);

constraint forall(j in J)(sum(i in I)(W[i] * x[i,j]) <= C * used[j]);



solve minimize sum(j in J)(used[j]);




