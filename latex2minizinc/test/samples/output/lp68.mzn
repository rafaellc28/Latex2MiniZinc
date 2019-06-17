array[1..N] of float: A;

int: N;

float: B;


array[1..N] of var bool: x;


constraint sum(j in 1..N)(A[j] * x[j]) <= B;



solve maximize sum(j in 1..N)(A[j] * x[j]);




