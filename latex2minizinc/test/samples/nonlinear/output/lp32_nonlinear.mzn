set of int: I = 1..14;

array[I] of float: a;

array[I] of float: c;


array[I] of var float: x = array1d(I, [0.01 | i in I]);


constraint forall(i in I)(x[i] >= 0);

constraint sum(i in I)(c[i] * x[i]) = 1;

constraint forall(i in 1..5)(x[i] <= 0.04);

constraint forall(i in 6..14)(x[i] <= 0.03);



solve minimize sum(i in I)(a[i] / x[i]);




