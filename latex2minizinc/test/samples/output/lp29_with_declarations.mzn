set of int: X = 1..N;

array[INDEX_SET_U_1] of set of int: U = array1d(INDEX_SET_U_1, [0..min(B,min(N - x,x - 1)) | x in X]);

int: T = 5;

float: p = 0.55;

float: q = 1 - p;

int: N = 50;

float: B = N;


array[INDEX_SET_V_1, INDEX_SET_V_2] of var float: V;

set of int: INDEX_SET_U_1;

set of int: INDEX_SET_V_1 = 0..T;

set of int: INDEX_SET_V_2;


constraint forall(t in INDEX_SET_V_1, x in X)(V[t,x] >= 0);

constraint forall(t in 0..floor(T - 1), x in 1..N, u in U[x])(V[t,x] >= p * V[t + 1,x + to_enum(X,u)] + q * V[t + 1,x - to_enum(X,u)]);

constraint forall(x in X)(V[T,x] = ln(x));



var float: obj = sum(t in 0..floor(T - 1), x in X)(V[t,x]);

solve minimize obj;




