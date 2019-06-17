array[1..4] of var float: x;


constraint forall(i0 in 1..4)(x[i0] <= 5);





solve minimize pow((x[1] + 10 * x[2]),2) + 5 * pow((x[3] - x[4]),2) + pow((x[2] - 2 * x[3]),4) + 10 * pow((x[1] - x[4]),4);




