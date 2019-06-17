set of int: I = 1..11;

array[I] of float: a;

array[I] of float: b = array1d(I, [1 / c[i] | i in I]);

array[I] of float: c;


array[1..4] of var float: x = array1d(1..4, [0.42 | i0 in 1..4]);


constraint forall(i0 in 1..4)(x[i0] >= 0 /\ x[i0] <= 0.42);





solve minimize sum(i in I)(pow((a[i] - x[1] * (pow(b[i],2) + b[i] * x[2]) / (pow(b[i],2) + b[i] * x[3] + x[4])),2));




