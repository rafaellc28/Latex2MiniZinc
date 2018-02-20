array[INDEX_SET_x_1] of var float: x;

var float: f1;

var float: f2;

set of int: INDEX_SET_x_1 = 1..2;


constraint f1 = 10 * (x[2] - pow(x[1],2));

constraint f2 = 1 - x[1];





solve minimize pow(f1,2) + pow(f2,2);




