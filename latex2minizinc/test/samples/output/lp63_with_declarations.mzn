set of int: V = i_i_j_in_E_union_j_i_j_in_E;

array[INDEX_SET_E, 1..2] of V: E;

array[V] of float: w = array1d(V, [1 | i in V]);


array[V] of var bool: x;

set of int: INDEX_SET_E;

set of int: INDEX_SET_i_i_j_in_E_union_j_i_j_in_E;

array[INDEX_SET_i_i_j_in_E_union_j_i_j_in_E] of int: i_i_j_in_E_union_j_i_j_in_E;


constraint forall(i in INDEX_SET_E)(x[E[i,1]] + x[E[i,2]] >= 1);



solve minimize sum(i in V)(w[i] * x[i]);




