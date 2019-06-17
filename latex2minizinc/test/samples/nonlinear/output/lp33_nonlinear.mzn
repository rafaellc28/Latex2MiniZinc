set of int: I = 1..5;


array[I] of var float: x = array1d(I, [0.4 | i in I]);


constraint forall(i in I)(x[i] <= 0.4);





solve minimize sum(i in I)(pow(x[i],10));




