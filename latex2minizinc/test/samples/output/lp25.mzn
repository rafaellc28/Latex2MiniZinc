array[INDEX_SET_E, 1..2] of int: E;

enum V;

array[int, int] of float: C;

int: N;

set of int: INDEX_SET_E;


array[int, int] of var bool: x;

array[int, int] of var float: y;


constraint forall(i in INDEX_SET_E)(y[E[i,1],E[i,2]] >= 0);

constraint forall(i in V)(sum(i in INDEX_SET_E)(x[E[i,1],E[i,2]]) = 1);

constraint forall(j in V)(sum(i in INDEX_SET_E)(x[E[i,1],E[i,2]]) = 1);

constraint forall(i in INDEX_SET_E)(y[E[i,1],E[i,2]] <= (N - 1) * x[E[i,1],E[i,2]]);

constraint forall(i in V)(sum(j in INDEX_SET_E)(y[E[j,1],E[j,2]] + (if E[j,2] = 1 then N else 0 endif)) = sum(i in INDEX_SET_E)(y[E[i,1],E[i,2]] + 1));



var float: obj = sum(i in INDEX_SET_E)(C[E[i,1],E[i,2]] * x[E[i,1],E[i,2]]);

solve minimize obj;




