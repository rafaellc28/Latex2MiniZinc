array[INDEX_SET_E, 1..2] of V: E;

set of int: V = i_i_j_in_E_union_j_i_j_in_E;

array[INDEX_SET_w_1, INDEX_SET_w_2] of float: w = array2d(INDEX_SET_w_1, INDEX_SET_w_2, [1 | i in INDEX_SET_E]);


array[V] of var bool: x;

array[INDEX_SET_t_1, INDEX_SET_t_2] of var bool: t;

set of int: INDEX_SET_E;

set of int: INDEX_SET_i_i_j_in_E_union_j_i_j_in_E;

set of int: INDEX_SET_t_1 = E;

set of int: INDEX_SET_t_2;

set of int: INDEX_SET_w_1;

set of int: INDEX_SET_w_2;

array[INDEX_SET_i_i_j_in_E_union_j_i_j_in_E] of int: i_i_j_in_E_union_j_i_j_in_E;


constraint forall(i in INDEX_SET_E)(x[E[i,1]] + x[E[i,2]] - 2 * t[E[i,1],E[i,2]] <= 1 /\ x[E[i,1]] + x[E[i,2]] - 2 * t[E[i,1],E[i,2]] >= 0);

constraint forall(i in V)(x[i] >= 0);



solve maximize sum(i in INDEX_SET_E)(w[E[i,1],E[i,2]] * (x[E[i,1]] + x[E[i,2]] - 2 * t[E[i,1],E[i,2]]));




