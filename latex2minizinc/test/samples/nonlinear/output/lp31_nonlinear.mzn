array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_x_1 = 1..2;


constraint x[1] * x[2] - 25 >= 0;

constraint pow(x[1],2) + pow(x[2],2) - 25 >= 0;

constraint x[1] >= 2;



var float: obj = 0.01 * pow(x[1],2) + pow(x[2],2);

solve minimize obj;




