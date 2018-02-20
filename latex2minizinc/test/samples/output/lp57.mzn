array[INDEX_SET_E, 1..2] of V: E;

enum V;

array[int, int] of float: W;


array[INDEX_SET_x_1] of var bool: x;

array[INDEX_SET_t_1, INDEX_SET_t_2] of var bool: t;

set of int: INDEX_SET_E;

set of int: INDEX_SET_t_1;

set of int: INDEX_SET_t_2;

set of int: INDEX_SET_x_1;


constraint forall(i in INDEX_SET_E)(x[E[i,1]] + x[E[i,2]] - 2 * t[E[i,1],E[i,2]] <= 1 /\ x[E[i,1]] + x[E[i,2]] - 2 * t[E[i,1],E[i,2]] >= 0);

constraint forall(i in V)(x[i] >= 0);



solve maximize sum(i in INDEX_SET_E)(W[E[i,1],E[i,2]] * (x[E[i,1]] + x[E[i,2]] - 2 * t[E[i,1],E[i,2]]));




