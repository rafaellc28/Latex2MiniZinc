enum C;

enum N;

array[int, int] of float: Data;

array[int] of float: Allowance;


array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_x_1 = C;


constraint forall(c in INDEX_SET_x_1)(x[c] >= 0);

constraint forall(n in N)(sum(c in C)(Data[c,n] * x[c]) >= Allowance[n]);



solve minimize sum(c in C)(x[c]);




