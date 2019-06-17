array[1..2] of var float: x = array1d(1..2, [1 | i0 in 1..2]);


constraint forall(i0 in 1..2)(x[i0] <= 100);





solve minimize (pow(x[1],2) + pow(x[2],2)) / 200 - cos(x[1]) * cos(x[2] / sqrt(2)) + 1;




