enum X;

array[INDEX_SET_U] of set of int: U;

int: T;

float: P;

float: Q;

int: N;


array[INDEX_SET_V_1, INDEX_SET_V_2] of var float: V;

set of int: INDEX_SET_U;

set of int: INDEX_SET_V_1 = 0..T;

set of int: INDEX_SET_V_2;


constraint forall(t in INDEX_SET_V_1, x in X)(V[t,x] >= 0);

constraint forall(t in 0..floor(T - 1), x in 1..N, u in U[to_enum(X,x)])(V[t,to_enum(X,x)] >= P * V[t + 1,to_enum(X,x) + to_enum(X,u)] + Q * V[t + 1,to_enum(X,x) - to_enum(X,u)]);

constraint forall(x in X)(V[T,x] = ln(x));

constraint forall(t in 0..T, x in X)(V[t,x] >= 0);

constraint forall(x in X, u in U[x])(to_enum(X,u) >= 0);



solve minimize sum(t in 0..floor(T - 1), x in X)(V[t,x]);




