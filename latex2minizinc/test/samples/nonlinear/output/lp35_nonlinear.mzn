array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_x_1 = 1..2;


constraint forall(i0 in INDEX_SET_x_1)(x[i0] <= 5);





var float: obj = pow(x[1],4) + 4 * pow(x[1],3) + 4 * pow(x[1],2) + pow(x[2],2);

solve minimize obj;




