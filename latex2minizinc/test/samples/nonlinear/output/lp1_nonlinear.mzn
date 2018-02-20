float: pi = 4 * atan(1);


array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_x_1 = 1..2;


constraint x[1] <= 10 /\ x[1] >= -5;

constraint x[2] <= 15 /\ x[2] >= 0;



solve minimize pow((x[2] - 5.1 * pow(x[1],2) / (4 * pi * pi) + 5 * x[1] / pi - 6),2) + 10 * (1 - 1 / (8 * pi)) * cos(x[1]) + 10;




