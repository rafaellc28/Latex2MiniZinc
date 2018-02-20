array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_x_1 = 1..2;


constraint forall(i0 in INDEX_SET_x_1)(x[i0] <= 10);





solve minimize pow((2 * pow(x[1],3) * x[2] - pow(x[2],3)),2) + pow((6 * x[1] - pow(x[2],2) + x[2]),2);




