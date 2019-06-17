enum C;


array[1..3, 2..4, 2..6] of var int: x;


constraint forall(i0 in 1..3, i1 in 2..4, i2 in 2..6)(x[i0,i1,i2] >= 0);

constraint x[1,3,5] + x[1,4,6] <= 80;

constraint x[3,2,4] + x[3,2,5] <= 100;



solve maximize sum(c in C)(3 * x[1,c,2] + 2 * x[2,2,c]);




