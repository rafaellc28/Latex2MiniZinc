array[1..3] of var float: x;


constraint forall(i0 in 1..3)(x[i0] >= 0);

constraint 3 >= x[1] + x[2] + 2 * x[3];



solve minimize 9 - 8 * x[1] - 6 * x[2] - 4 * x[3] + 2 * x[1] * x[1] + 2 * x[2] * x[2] + x[3] * x[3] + 2 * x[1] * x[2] + 2 * x[1] * x[3];




