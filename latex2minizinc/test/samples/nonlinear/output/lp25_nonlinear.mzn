set of int: I = 1..2;


array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_x_1;


constraint forall(i in I)(x[i] <= 10);





var float: obj = -product(i in I)(sum(j in 1..5)((j * cos((j + 1) * x[i] + j))));

solve minimize obj;




