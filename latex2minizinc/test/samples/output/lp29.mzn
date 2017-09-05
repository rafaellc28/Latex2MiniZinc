enum X;

array[INDEX_SET_U] of set of int: U;

int: T;

float: P;

float: Q;

int: N;

set of int: INDEX_SET_U;


array[int, int] of var float: V;


constraint forall(t in 0..T, x in X)(V[t,x] >= 0);

constraint forall(t in 0..T - 1, x in 1..N, u in U[to_enum(X,x)])(V[t,to_enum(X,x)] >= P * V[t + 1,to_enum(X,x) + to_enum(X,u)] + Q * V[t + 1,to_enum(X,x) - to_enum(X,u)]);

constraint forall(x in X)(V[T,x] = ln(x));

constraint forall(t in 0..T, x in X)(V[t,x] >= 0);

constraint forall(x in X, u in U[x])(to_enum(X,u) >= 0);



var float: obj = sum(t in 0..T - 1, x in X)(V[t,x]);

solve minimize obj;




