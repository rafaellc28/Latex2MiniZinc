array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_x_1 = 1..2;


constraint x[1] * x[1] + x[2] * x[2] = 25;

constraint x[1] * x[2] = 9;



var float: obj = -1;

solve minimize obj;




