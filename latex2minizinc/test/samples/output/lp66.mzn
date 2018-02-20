array[INDEX_SET_C] of set of int: C;

int: M;

int: N;


array[INDEX_SET_y_1] of var bool: y;

array[INDEX_SET_x_1] of var bool: x;

set of int: INDEX_SET_C;

set of int: INDEX_SET_x_1 = 1..N;

set of int: INDEX_SET_y_1 = 1..M;


constraint forall(i in 1..M)(sum(j in C[i])((if j > 0 then x[j] else (1 - x[-j]) endif) + y[i]) >= 1);

constraint forall(j in 1..N)(x[j] >= 0);



solve minimize sum(i in 1..M)(y[i]);




