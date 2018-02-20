array[INDEX_SET_C] of set of int: C;

int: m;

int: n;


array[INDEX_SET_x_1] of var bool: x;

array[INDEX_SET_y_1] of var bool: y;

set of int: INDEX_SET_C;

set of int: INDEX_SET_x_1 = 1..n;

set of int: INDEX_SET_y_1 = 1..m;


constraint forall(i in 1..m)(sum(j in C[i])((if j > 0 then x[j] else (1 - x[-j]) endif) + y[i]) >= 1);



solve minimize sum(i in 1..m)(y[i]);




