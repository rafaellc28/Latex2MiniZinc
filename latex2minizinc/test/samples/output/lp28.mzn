enum X;

array[INDEX_SET_U] of set of int: U;

float: A;

float: P;

float: Q;

X: N;

set of int: INDEX_SET_U;


array[int] of var float: V;


constraint forall(x in 1..N - 1, u in U[to_enum(X,x)])(V[to_enum(X,x)] >= A * (P * V[to_enum(X,x) + to_enum(X,u)] + Q * V[to_enum(X,x) - to_enum(X,u)]));

constraint V[0] = 0;

constraint V[N] = N;

constraint forall(x in X)(V[x] >= 0);

constraint forall(x in X, u in U[x])(to_enum(X,u) >= 0);



var float: obj = sum(x in X)(V[x]);

solve minimize obj;




