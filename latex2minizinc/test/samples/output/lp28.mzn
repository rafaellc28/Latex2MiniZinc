enum X;

array[INDEX_SET_U] of set of int: U;

float: A;

float: P;

float: Q;

X: N;


array[INDEX_SET_V_1] of var float: V;

set of int: INDEX_SET_U;

set of int: INDEX_SET_V_1;


constraint forall(x in 1..floor(N - 1), u in U[to_enum(X,x)])(V[to_enum(X,x)] >= A * (P * V[to_enum(X,x) + to_enum(X,u)] + Q * V[to_enum(X,x) - to_enum(X,u)]));

constraint V[0] = 0;

constraint V[N] = N;

constraint forall(x in X)(V[x] >= 0);

constraint forall(x in X, u in U[x])(to_enum(X,u) >= 0);



solve minimize sum(x in X)(V[x]);




