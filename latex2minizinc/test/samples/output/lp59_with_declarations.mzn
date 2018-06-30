array[INDEX_SET_E, 1..2] of V: E;

set of int: V = 1..n;

int: n;


array[INDEX_SET_k_1] of var float: k;

array[INDEX_SET_x_1, INDEX_SET_x_2] of var bool: x;

set of int: INDEX_SET_E;

set of int: INDEX_SET_k_1 = V;

set of int: INDEX_SET_x_1 = E;

set of int: INDEX_SET_x_2;


constraint assert(n >= 0, "Assertion n >= 0 failed!");

constraint forall(i in INDEX_SET_k_1)(k[i] >= 1);

constraint forall(i in INDEX_SET_k_1)(k[i] <= card(V));

constraint forall(i in INDEX_SET_E)(k[E[i,2]] - k[E[i,1]] >= 1 - card(V) * x[E[i,1],E[i,2]]);



solve minimize sum(i in INDEX_SET_E)(x[E[i,1],E[i,2]]);




