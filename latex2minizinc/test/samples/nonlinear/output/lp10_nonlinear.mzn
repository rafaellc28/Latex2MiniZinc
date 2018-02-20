set of int: I = 1..10;

array[int] of float: c;


array[INDEX_SET_x_1] of var float: x = array1d(I, [-2.3 | k in I]);

set of int: INDEX_SET_x_1;


constraint forall(k in I)(x[k] <= 100);

constraint exp(x[1]) + 2 * exp(x[2]) + 2 * exp(x[3]) + exp(x[6]) + exp(x[10]) = 2;

constraint exp(x[4]) + 2 * exp(x[5]) + exp(x[6]) + exp(x[7]) = 1;

constraint exp(x[3]) + exp(x[7]) + exp(x[8]) + 2 * exp(x[9]) + exp(x[10]) = 1;



solve minimize sum(i in I)(exp(x[i]) * (c[i] + x[i] - ln(sum(k in I)(exp(x[k])))));




