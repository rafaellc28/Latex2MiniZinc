array[1..3] of var float: x = array1d(1..3, [1 | i0 in 1..3]);


constraint forall(i0 in 1..3)(x[i0] >= 1E-5);

constraint 1 >= 4 / x[1] + 32 / x[2] + 120 / x[3];



solve minimize 5 * x[1] + 50000 / x[1] + 20 * x[2] + 72000 / x[2] + 10 * x[3] + 144000 / x[3];




