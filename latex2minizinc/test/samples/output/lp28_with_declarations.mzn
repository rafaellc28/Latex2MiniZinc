set of int: X = 0..N;

array[INDEX_SET_U_1] of set of int: U = array1d(INDEX_SET_U_1, [1..min(B,min(N - x,x)) | x in X]);

float: a = 1;

float: p = 0.25;

float: q = 1 - p;

int: N = 100;

float: B = N;


array[INDEX_SET_V_1] of var float: V;

set of int: INDEX_SET_U_1;

set of int: INDEX_SET_V_1;


constraint forall(x in 1..floor(N - 1), u in U[x])(V[x] >= a * (p * V[x + u] + q * V[x - u]));

constraint V[0] = 0;

constraint V[N] = N;



solve minimize sum(x in X)(V[x]);




