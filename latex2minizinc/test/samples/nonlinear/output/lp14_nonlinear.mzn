array[1..2] of var float: x;


constraint x[1] * x[2] - 1 >= 0;

constraint x[1] + x[2] * x[2] >= 0;

constraint x[1] <= 0.5;



solve minimize 100 * pow((x[2] - pow(x[1],2)),2) + pow((1 - x[1]),2);




