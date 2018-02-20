enum J;

enum I;

array[int] of float: W;

float: C;


array[INDEX_SET_used_1] of var bool: used;

array[INDEX_SET_x_1, INDEX_SET_x_2] of var bool: x;

set of int: INDEX_SET_used_1;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;


constraint forall(i in I)(sum(j in J)(x[i,j]) = 1);

constraint forall(j in J)(sum(i in I)(W[i] * x[i,j]) <= C * used[j]);



solve minimize sum(j in J)(used[j]);




