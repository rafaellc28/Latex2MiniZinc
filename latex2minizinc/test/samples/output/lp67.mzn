array[INDEX_SET_E, 1..2] of int: E;

array[int, int] of float: C;

float: S;

float: T;

int: N;


array[INDEX_SET_x_1, INDEX_SET_x_2] of var float: x;

set of int: INDEX_SET_E;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;


constraint forall(i in INDEX_SET_E)(x[E[i,1],E[i,2]] >= 0);

constraint forall(i in 1..N)(sum(j in INDEX_SET_E)(x[E[j,1],E[j,2]] + (if E[j,2] = S then 1 else 0 endif)) = sum(i in INDEX_SET_E)(x[E[i,1],E[i,2]] + (if E[i,1] = T then 1 else 0 endif)));



var float: obj = sum(i in INDEX_SET_E)(C[E[i,1],E[i,2]] * x[E[i,1],E[i,2]]);

solve minimize obj;




