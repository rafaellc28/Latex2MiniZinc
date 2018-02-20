array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_x_1 = 1..4;


constraint forall(i0 in INDEX_SET_x_1)(x[i0] >= 0);

constraint 8 - x[1] - 2 * x[2] >= 0;

constraint 12 - 4 * x[1] - x[2] >= 0;

constraint 12 - 3 * x[1] - 4 * x[2] >= 0;

constraint 8 - 2 * x[3] - x[4] >= 0;

constraint 8 - x[3] - 2 * x[4] >= 0;

constraint 5 - x[3] - x[4] >= 0;



solve minimize x[1] - x[2] - x[3] - x[1] * x[3] + x[1] * x[4] + x[2] * x[3] - x[2] * x[4];




