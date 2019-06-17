enum N;

int: C;


array[1..C, 1..C, N] of var bool: x;

var float: s;


constraint forall(i in 1..C, j in 1..C)(sum(k in N)(x[i,j,k]) = 1);

constraint forall(k in N)(sum(i in 1..C, j in 1..C)(x[i,j,k]) = 1);

constraint forall(i in 1..C)(sum(j in 1..C, k in N)(k * x[i,j,k]) = s);

constraint forall(j in 1..C)(sum(i in 1..C, k in N)(k * x[i,j,k]) = s);

constraint sum(i in 1..C, k in N)(k * x[i,i,k]) = s;

constraint sum(i in 1..C, k in N)(k * x[i,C - i + 1,k]) = s;

solve satisfy;


