set of int: I = 1..10;

array[I] of float: c;


array[I] of var float: x = array1d(I, [0.1 | k in I]);


constraint forall(k in I)(x[k] >= 1e-6);

constraint x[1] + 2 * x[2] + 2 * x[3] + x[6] + x[10] = 2;

constraint x[4] + 2 * x[5] + x[6] + x[7] = 1;

constraint x[3] + x[7] + x[8] + 2 * x[9] + x[10] = 1.5;



solve minimize sum(i in I)(x[i] * (c[i] + ln(x[i] / (sum(k in I)(x[k])))));




