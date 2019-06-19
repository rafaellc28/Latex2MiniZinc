enum X;

array[INDEX_SET_U] of set of int: U;

float: A;

float: P;

float: Q;

X: N;


array[X] of var float: V;

set of int: INDEX_SET_U;


constraint forall(x in 1..floor(N - 1), u in U[x])(V[to_enum(X,x)] >= A * (P * V[to_enum(X,x + u)] + Q * V[to_enum(X,x - u)]));

constraint V[to_enum(X,0)] = 0;

constraint V[N] = N;

constraint forall(x in X)(V[x] >= 0);

constraint forall(x in X, u in U[x])(u >= 0);



solve minimize sum(x in X)(V[x]);




