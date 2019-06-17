array[1..2] of var float: x;


constraint forall(i0 in 1..2)(x[i0] <= 10);





solve minimize pow((2 * pow(x[1],3) * x[2] - pow(x[2],3)),2) + pow((6 * x[1] - pow(x[2],2) + x[2]),2);




