set of int: V = 1..n;

array[INDEX_SET_E, 1..2] of int: E;

int: n;


array[V] of var bool: x;

array[V] of var float: k;

set of int: INDEX_SET_E;


constraint assert(n >= 0, "Assertion n >= 0 failed!");

constraint forall(i in V)(k[i] >= 1);

constraint forall(i in V)(k[i] <= card(V));

constraint forall(i in INDEX_SET_E)(k[E[i,2]] - k[E[i,1]] >= 1 - card(V) * (x[E[i,1]] + x[E[i,2]]));



solve minimize sum(i in V)(x[i]);




