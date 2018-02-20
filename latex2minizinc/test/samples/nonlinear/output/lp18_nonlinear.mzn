array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_x_1 = 1..2;


constraint x[1] <= 4 /\ x[1] >= -1.5;

constraint x[2] <= 3 /\ x[2] >= -3;



solve minimize sin(x[1] + x[2]) + pow((x[1] - x[2]),2) - 1.5 * x[1] + 2.5 * x[2] + 1;




