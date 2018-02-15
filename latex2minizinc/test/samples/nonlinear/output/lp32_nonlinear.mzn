set of int: I = 1..14;

array[int] of float: a;

array[int] of float: c;


array[INDEX_SET_x_1] of var float: x = array1d(I, [0.01 | i in I]);

set of int: INDEX_SET_x_1;


constraint forall(i in I)(x[i] >= 0);

constraint sum(i in I)(c[i] * x[i]) = 1;

constraint forall(i in 1..5)(x[i] <= 0.04);

constraint forall(i in 6..14)(x[i] <= 0.03);



var float: obj = sum(i in I)(a[i] / x[i]);

solve minimize obj;




