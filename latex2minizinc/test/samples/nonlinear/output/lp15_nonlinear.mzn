array[1..2] of var float: x;


constraint forall(i0 in 1..2)(x[i0] <= 50);

constraint x[1] + x[2] - 1 >= 0;

constraint x[1] * x[1] + x[2] * x[2] - 1 >= 0;

constraint 9 * x[1] * x[1] + x[2] * x[2] - 9 >= 0;

constraint x[1] * x[1] - x[2] >= 0;

constraint x[2] * x[2] - x[1] >= 0;



solve minimize x[1] * x[1] + x[2] * x[2];




