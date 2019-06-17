int: M;

int: P;


array[M..9] of var int: x;


constraint forall(i in M..9)(x[i] >= 0);

constraint forall(i in 2..5)(x[i] + x[i + 1] <= 80);

constraint forall(i in M..9 where (i-M) mod P = 0)(x[i] + x[i + 1] <= 100);



solve maximize 3 * x[1] + 2 * x[10];




