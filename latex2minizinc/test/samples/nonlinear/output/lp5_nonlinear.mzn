array[1..2] of var float: x;


constraint forall(i0 in 1..2)(x[i0] <= 2);





solve minimize (1 + pow((x[1] + x[2] + 1),2) * (19 - 14 * x[1] + 3 * pow(x[1],2) - 14 * x[2] + 6 * x[1] * x[2] + 3 * pow(x[2],2))) * (30 + pow((2 * x[1] - 3 * x[2]),2) * (18 - 32 * x[1] + 12 * pow(x[1],2) + 48 * x[2] - 36 * x[1] * x[2] + 27 * pow(x[2],2)));




