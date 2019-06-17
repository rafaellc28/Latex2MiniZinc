array[1..2] of var float: x;


constraint 10 * (x[2] - pow(x[1],2)) = 0;



solve minimize pow((1 - x[1]),2);




