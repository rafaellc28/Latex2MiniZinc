array[1..2] of var float: x;


constraint x[1] * x[1] + x[2] * x[2] = 25;

constraint x[1] * x[2] = 9;



solve minimize -1;




