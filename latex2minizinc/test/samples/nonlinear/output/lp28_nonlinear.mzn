array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_x_1 = 1..4;


constraint forall(i0 in INDEX_SET_x_1)(x[i0] <= 5);





var float: obj = pow((x[1] + 10 * x[2]),2) + 5 * pow((x[3] - x[4]),2) + pow((x[2] - 2 * x[3]),4) + 10 * pow((x[1] - x[4]),4);

solve minimize obj;




