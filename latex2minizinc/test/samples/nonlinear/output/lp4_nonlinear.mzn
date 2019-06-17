float: pi = 4 * atan(1);


array[1..2] of var float: x;


constraint x[1] <= 30 /\ x[1] >= -30;

constraint x[2] <= 10 /\ x[2] >= -10;



solve minimize pow(x[1],2) - 12 * x[1] + 11 + 10 * cos(pi * x[1] / 2) + 8 * sin(pi * 5 * x[1]) - exp(-pow((x[2] - 0.5),2) / 2) / sqrt(5);




