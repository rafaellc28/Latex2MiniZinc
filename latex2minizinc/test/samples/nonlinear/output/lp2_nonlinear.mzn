array[INDEX_SET_x_1] of var float: x = array1d(INDEX_SET_x_1, [1 | i0 in INDEX_SET_x_1]);

set of int: INDEX_SET_x_1 = 1..2;


constraint forall(i0 in INDEX_SET_x_1)(x[i0] <= 5);





solve minimize 4 * pow(x[1],2) - 2.1 * pow(x[1],4) + pow(x[1],6) / 3 + x[1] * x[2] - 4 * pow(x[2],2) + 4 * pow(x[2],4);




