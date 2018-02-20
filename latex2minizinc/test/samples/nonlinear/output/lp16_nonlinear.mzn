array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_x_1 = 1..3;


constraint forall(i0 in INDEX_SET_x_1)(x[i0] >= 0);

constraint 3 >= x[1] + x[2] + 2 * x[3];



solve minimize 9 - 8 * x[1] - 6 * x[2] - 4 * x[3] + 2 * x[1] * x[1] + 2 * x[2] * x[2] + x[3] * x[3] + 2 * x[1] * x[2] + 2 * x[1] * x[3];




