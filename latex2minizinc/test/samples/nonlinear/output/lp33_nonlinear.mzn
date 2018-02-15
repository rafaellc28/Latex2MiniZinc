set of int: I = 1..5;


array[INDEX_SET_x_1] of var float: x = array1d(I, [0.4 | i in I]);

set of int: INDEX_SET_x_1;


constraint forall(i in I)(x[i] <= 0.4);





var float: obj = sum(i in I)(pow(x[i],10));

solve minimize obj;




