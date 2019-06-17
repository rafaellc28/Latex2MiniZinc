set of int: I = 1..2;


array[I] of var float: x;


constraint forall(i in I)(x[i] <= 10);





solve minimize -product(i in I)(sum(j in 1..5)((j * cos((j + 1) * x[i] + j))));




