array[1..3, 1..6] of var int: x;


constraint forall(i0 in 1..3, i1 in 1..6)(x[i0,i1] >= 0);

constraint x[1,3] + x[1,6] <= 80;

constraint x[3,2] + x[3,2] <= 100;



solve maximize 3 * x[1,1] + 2 * x[2,2];




