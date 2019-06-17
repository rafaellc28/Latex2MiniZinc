enum V;

array[INDEX_SET_E, 1..2] of V: E;

array[V] of float: W;


array[V] of var bool: x;

set of int: INDEX_SET_E;


constraint forall(i in INDEX_SET_E)(x[to_enum(V,E[i,1])] + x[to_enum(V,E[i,2])] >= 1);



solve minimize sum(i in V)(W[i] * x[i]);




