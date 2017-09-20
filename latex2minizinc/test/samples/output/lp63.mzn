enum V;

array[INDEX_SET_E, 1..2] of V: E;

array[int] of float: W;


array[INDEX_SET_x_1] of var bool: x;

set of int: INDEX_SET_E;

set of int: INDEX_SET_x_1;


constraint forall(i in INDEX_SET_E)(x[E[i,1]] + x[E[i,2]] >= 1);



var float: obj = sum(i in V)(W[i] * x[i]);

solve minimize obj;




