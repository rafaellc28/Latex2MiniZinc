int: M;


array[INDEX_SET_x_1] of var int: x;

set of int: INDEX_SET_x_1 = M..10;


constraint forall(i in INDEX_SET_x_1)(x[i] >= 0);

constraint forall(i in 2..5)(x[i] + x[i + 1] <= 80);

constraint forall(i in M..9)(x[i] + x[i + 1] <= 100);



solve maximize 3 * x[1] + 2 * x[10];




