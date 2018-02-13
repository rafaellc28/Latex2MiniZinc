set of int: J = 1..M;

set of int: I = 1..N;

array[int] of float: y;

array[INDEX_SET_t_1] of float: t = array1d(INDEX_SET_t_1, [10 * (j - 1) | j in J]);

int: N;

int: M;


array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_t_1;

set of int: INDEX_SET_x_1;


constraint forall(i in I)(x[i] <= 10);





var float: obj = sum(j in J)(pow((y[j] - (x[1] + x[2] * exp(-t[j] * x[4]) + x[3] * exp(-t[j] * x[5]))),2));

solve minimize obj;




