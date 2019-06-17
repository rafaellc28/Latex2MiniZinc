set of int: X = 0..N;

array[X] of set of int: U = array1d(X, [1..floor(min(B,min(N - x,x))) | x in X]);

float: a = 1;

float: p = 0.25;

float: q = 1 - p;

int: N = 100;

float: B = N;


array[X] of var float: V;


constraint forall(x in 1..floor(N - 1), u in U[x])(V[x] >= a * (p * V[x + u] + q * V[x - u]));

constraint V[0] = 0;

constraint V[N] = N;



solve minimize sum(x in X)(V[x]);




