set of int: N = 1..floor(pow(n,2));

int: n = 4;


array[1..n, 1..n, N] of var bool: x;

var float: s;


constraint forall(i in 1..n, j in 1..n)(sum(k in N)(x[i,j,k]) = 1);

constraint forall(k in N)(sum(i in 1..n, j in 1..n)(x[i,j,k]) = 1);

constraint forall(i in 1..n)(sum(j in 1..n, k in N)(k * x[i,j,k]) = s);

constraint forall(j in 1..n)(sum(i in 1..n, k in N)(k * x[i,j,k]) = s);

constraint sum(i in 1..n, k in N)(k * x[i,i,k]) = s;

constraint sum(i in 1..n, k in N)(k * x[i,n - i + 1,k]) = s;

solve satisfy;


