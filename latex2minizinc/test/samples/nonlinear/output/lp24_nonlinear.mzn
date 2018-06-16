set of int: I = 1..11;

array[int] of float: a;

array[INDEX_SET_b_1] of float: b = array1d(INDEX_SET_b_1, [1 / c[i] | i in I]);

array[int] of float: c;


array[INDEX_SET_x_1] of var float: x = array1d(INDEX_SET_x_1, [0.42 | i0 in INDEX_SET_x_1]);

set of int: INDEX_SET_b_1;

set of int: INDEX_SET_x_1 = 1..4;


constraint forall(i0 in INDEX_SET_x_1)(x[i0] >= 0 /\ x[i0] <= 0.42);





solve minimize sum(i in I)(pow((a[i] - x[1] * (pow(b[i],2) + b[i] * x[2]) / (pow(b[i],2) + b[i] * x[3] + x[4])),2));




