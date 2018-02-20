array[INDEX_SET_E, 1..2] of V: E;

enum V;


array[INDEX_SET_x_1, INDEX_SET_x_2] of var bool: x;

array[INDEX_SET_k_1] of var float: k;

set of int: INDEX_SET_E;

set of int: INDEX_SET_k_1;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;


constraint forall(i in V)(k[i] >= 1);

constraint forall(i in INDEX_SET_E)(k[E[i,2]] - k[E[i,1]] >= 1 - card(V) * x[E[i,1],E[i,2]]);

constraint forall(i in V)(k[i] <= card(V));



solve minimize sum(i in INDEX_SET_E)(x[E[i,1],E[i,2]]);




