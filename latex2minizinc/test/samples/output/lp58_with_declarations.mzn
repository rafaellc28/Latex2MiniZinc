array[INDEX_SET_E, 1..2] of int: E;

set of int: V = 1..n;

int: s = 1;

int: t = n;

array[int, int] of float: a;

int: n;


var float: flow;

array[INDEX_SET_x_1, INDEX_SET_x_2] of var float: x;

set of int: INDEX_SET_E;

set of int: INDEX_SET_x_1 = E;

set of int: INDEX_SET_x_2;


constraint flow >= 0;

constraint forall(i in INDEX_SET_E)(x[E[i,1],E[i,2]] >= 0);

constraint forall(i in INDEX_SET_E)(x[E[i,1],E[i,2]] <= a[E[i,1],E[i,2]]);

constraint forall(i in V)(sum(j in INDEX_SET_E)(x[E[j,1],E[j,2]] + (if E[j,2] = s then flow else 0 endif)) = sum(i in INDEX_SET_E)(x[E[i,1],E[i,2]] + (if E[i,1] = t then flow else 0 endif)));

constraint forall(i in INDEX_SET_E)(x[E[i,1],E[i,2]] <= a[E[i,1],E[i,2]]);



solve maximize flow;




