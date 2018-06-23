array[INDEX_SET_E, 1..2] of int: E;

set of int: V = 1..n;

array[int, int] of float: c;

int: n;


array[INDEX_SET_x_1, INDEX_SET_x_2] of var bool: x;

array[INDEX_SET_y_1, INDEX_SET_y_2] of var float: y;

set of int: INDEX_SET_E;

set of int: INDEX_SET_x_1 = E;

set of int: INDEX_SET_x_2;

set of int: INDEX_SET_y_1 = E;

set of int: INDEX_SET_y_2;


constraint forall(i in INDEX_SET_E)(y[E[i,1],E[i,2]] >= 0);

constraint forall(i in V)(sum(i in INDEX_SET_E)(x[E[i,1],E[i,2]]) = 1);

constraint forall(j in V)(sum(i in INDEX_SET_E)(x[E[i,1],E[i,2]]) = 1);

constraint forall(i in INDEX_SET_E)(y[E[i,1],E[i,2]] <= (n - 1) * x[E[i,1],E[i,2]]);

constraint forall(i in V)(sum(j in INDEX_SET_E)(y[E[j,1],E[j,2]] + (if E[j,2] = 1 then n else 0 endif)) = sum(i in INDEX_SET_E)(y[E[i,1],E[i,2]] + 1));



solve minimize sum(i in INDEX_SET_E)(c[E[i,1],E[i,2]] * x[E[i,1],E[i,2]]);




