array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_x_1 = 1..2;


constraint x[1] * x[2] - 1 >= 0;

constraint x[1] + x[2] * x[2] >= 0;

constraint x[1] <= 0.5;



var float: obj = 100 * pow((x[2] - pow(x[1],2)),2) + pow((1 - x[1]),2);

solve minimize obj;




