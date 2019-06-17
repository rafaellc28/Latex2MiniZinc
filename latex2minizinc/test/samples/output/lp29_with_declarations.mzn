set of int: X = 1..N;

array[X] of set of int: U = array1d(X, [0..floor(min(B,min(N - x,x - 1))) | x in X]);

int: T = 5;

float: p = 0.55;

float: q = 1 - p;

int: N = 50;

float: B = N;


array[0..T, X] of var float: V;


constraint forall(t in 0..T, x in X)(V[t,x] >= 0);

constraint forall(t in 0..floor(T - 1), x in 1..N, u in U[x])(V[t,x] >= p * V[t + 1,x + u] + q * V[t + 1,x - u]);

constraint forall(x in X)(V[T,x] = ln(x));



solve minimize sum(t in 0..floor(T - 1), x in X)(V[t,x]);




