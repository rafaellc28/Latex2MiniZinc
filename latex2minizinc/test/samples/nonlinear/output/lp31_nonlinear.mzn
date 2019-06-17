array[1..2] of var float: x = array1d(1..2, [2 | i0 in 1..2]);


constraint x[1] * x[2] - 25 >= 0;

constraint pow(x[1],2) + pow(x[2],2) - 25 >= 0;

constraint x[1] >= 2;



solve minimize 0.01 * pow(x[1],2) + pow(x[2],2);




