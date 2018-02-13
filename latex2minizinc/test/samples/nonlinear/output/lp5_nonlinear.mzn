array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_x_1 = 1..2;


constraint forall(i0 in INDEX_SET_x_1)(x[i0] <= 2);





var float: obj = (1 + pow((x[1] + x[2] + 1),2) * (19 - 14 * x[1] + 3 * pow(x[1],2) - 14 * x[2] + 6 * x[1] * x[2] + 3 * pow(x[2],2))) * (30 + pow((2 * x[1] - 3 * x[2]),2) * (18 - 32 * x[1] + 12 * pow(x[1],2) + 48 * x[2] - 36 * x[1] * x[2] + 27 * pow(x[2],2)));

solve minimize obj;




