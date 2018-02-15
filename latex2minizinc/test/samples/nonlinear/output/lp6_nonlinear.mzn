array[INDEX_SET_x_1] of var float: x = 1;

set of int: INDEX_SET_x_1 = 1..2;


constraint forall(i0 in INDEX_SET_x_1)(x[i0] <= 100);





var float: obj = (pow(x[1],2) + pow(x[2],2)) / 200 - cos(x[1]) * cos(x[2] / sqrt(2)) + 1;

solve minimize obj;




