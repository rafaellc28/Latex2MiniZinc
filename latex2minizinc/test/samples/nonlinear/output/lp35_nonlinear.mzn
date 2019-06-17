array[1..2] of var float: x;


constraint forall(i0 in 1..2)(x[i0] <= 5);





solve minimize pow(x[1],4) + 4 * pow(x[1],3) + 4 * pow(x[1],2) + pow(x[2],2);




