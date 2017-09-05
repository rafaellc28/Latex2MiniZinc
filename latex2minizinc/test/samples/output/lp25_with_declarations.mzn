array[INDEX_SET_E, 1..2] of int: E;

set of int: V = 1..n;

array[int, int] of float: c;

int: n;

set of int: INDEX_SET_E;

set of int: INDEX_SET_V_cross_V;

array[INDEX_SET_V_cross_V,1..2] of int: V_cross_V;


array[int, int] of var bool: x;

array[int, int] of var float: y;


constraint forall(i in INDEX_SET_E)(y[E[i,1],E[i,2]] >= 0);

constraint forall(i in V)(sum(i in INDEX_SET_E)(x[E[i,1],E[i,2]]) = 1);

constraint forall(j in V)(sum(i in INDEX_SET_E)(x[E[i,1],E[i,2]]) = 1);

constraint forall(i in INDEX_SET_E)(y[E[i,1],E[i,2]] <= (n - 1) * x[E[i,1],E[i,2]]);

constraint forall(i in V)(sum(j in INDEX_SET_E)(y[E[j,1],E[j,2]] + (if E[j,2] = 1 then n else 0 endif)) = sum(i in INDEX_SET_E)(y[E[i,1],E[i,2]] + 1));



var float: obj = sum(i in INDEX_SET_E)(c[E[i,1],E[i,2]] * x[E[i,1],E[i,2]]);

solve minimize obj;




