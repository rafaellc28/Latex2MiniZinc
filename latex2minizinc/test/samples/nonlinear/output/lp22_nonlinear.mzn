array[INDEX_SET_x_1] of var float: x = array1d(1..3, [1 | i0 in INDEX_SET_x_1]);

set of int: INDEX_SET_x_1 = 1..3;


constraint forall(i0 in INDEX_SET_x_1)(x[i0] >= 1E-5);

constraint 1 >= 4 / x[1] + 32 / x[2] + 120 / x[3];



var float: obj = 5 * x[1] + 50000 / x[1] + 20 * x[2] + 72000 / x[2] + 10 * x[3] + 144000 / x[3];

solve minimize obj;




