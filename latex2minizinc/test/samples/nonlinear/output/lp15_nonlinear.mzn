array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_x_1 = 1..2;


constraint forall(i0 in INDEX_SET_x_1)(x[i0] <= 50);

constraint x[1] + x[2] - 1 >= 0;

constraint x[1] * x[1] + x[2] * x[2] - 1 >= 0;

constraint 9 * x[1] * x[1] + x[2] * x[2] - 9 >= 0;

constraint x[1] * x[1] - x[2] >= 0;

constraint x[2] * x[2] - x[1] >= 0;



var float: obj = x[1] * x[1] + x[2] * x[2];

solve minimize obj;




