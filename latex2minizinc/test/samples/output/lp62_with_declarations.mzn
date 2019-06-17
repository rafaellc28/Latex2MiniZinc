set of int: V = 1..n;

array[INDEX_SET_E, 1..2] of int: E;

int: n;


array[V] of var bool: x;

set of int: INDEX_SET_E;


constraint assert(n > 0, "Assertion n > 0 failed!");

constraint forall(i in INDEX_SET_E)(x[E[i,1]] + x[E[i,2]] <= 1);



solve maximize sum(i in V)(x[i]);




