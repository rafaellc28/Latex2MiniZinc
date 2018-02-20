array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_x_1 = 1..2;


constraint 10 * (x[2] - pow(x[1],2)) = 0;



solve minimize pow((1 - x[1]),2);




