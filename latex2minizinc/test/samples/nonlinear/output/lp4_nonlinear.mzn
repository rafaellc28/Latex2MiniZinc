float: pi = 4 * atan(1);


array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_x_1 = 1..2;


constraint x[1] <= 30 /\ x[1] >= -30;

constraint x[2] <= 10 /\ x[2] >= -10;



var float: obj = pow(x[1],2) - 12 * x[1] + 11 + 10 * cos(pi * x[1] / 2) + 8 * sin(pi * 5 * x[1]) - exp(-pow((x[2] - 0.5),2) / 2) / sqrt(5);

solve minimize obj;




