set of int: V = i_i_j_in_E_union_j_i_j_in_E;

array[INDEX_SET_E, 1..2] of V: E;

array[INDEX_SET_w_1] of float: w = array1d(INDEX_SET_w_1, [1 | i in V]);


array[INDEX_SET_x_1] of var bool: x;

set of int: INDEX_SET_E;

set of int: INDEX_SET_i_i_j_in_E_union_j_i_j_in_E;

set of int: INDEX_SET_w_1;

set of int: INDEX_SET_x_1;

array[INDEX_SET_i_i_j_in_E_union_j_i_j_in_E] of int: i_i_j_in_E_union_j_i_j_in_E;


constraint forall(i in INDEX_SET_E)(x[E[i,1]] + x[E[i,2]] >= 1);



var float: obj = sum(i in V)(w[i] * x[i]);

solve minimize obj;




