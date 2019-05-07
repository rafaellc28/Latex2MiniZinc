array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_x_1 = 1..3;


constraint forall(i0 in INDEX_SET_x_1)(x[i0] >= 0 /\ x[i0] <= 1);

constraint x[1] + x[2] + x[3] = 1;



solve minimize -32.174 * (255 * log((x[1] + x[2] + x[3] + 0.03) / (0.09 * x[1] + x[2] + x[3] + 0.03)) + 280 * log((x[2] + x[3] + 0.03) / (0.07 * x[2] + x[3] + 0.03)) + 290 * log((x[3] + 0.03) / (0.13 * x[3] + 0.03)));




