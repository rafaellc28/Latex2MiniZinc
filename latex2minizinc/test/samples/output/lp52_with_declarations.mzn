set of int: V = 1..n;

array[INDEX_SET_E, 1..2] of int: E;

array[INDEX_SET_EE, 1..2] of int: EE = array2d(INDEX_SET_EE, 1..2, [if idx2 = 1 then E[i,1] else E[i,2] endif | i in INDEX_SET_E, idx2 in 1..2]) union array2d(INDEX_SET_EE, 1..2, [if idx2 = 1 then E[i,2] else E[i,1] endif | i in INDEX_SET_E, idx2 in 1..2]);

int: nc = max(i in V)(z[i,0]);

int: n;

array[V, 0..1] of int: z;


array[1..nc] of var bool: u;

array[V, 1..nc] of var bool: x;

set of int: INDEX_SET_E;

set of int: INDEX_SET_EE;


constraint assert(n >= 2, "Assertion n >= 2 failed!");

constraint forall(i in V, case in 0..1)(z[i,case] = (if case = 0 then (min(c in 1..z[i,1])((if not exists(j in V where j < i /\ i in INDEX_SET_EE)(z[j,0] = c) then c else z[i,1] + 1 endif))) else (if not exists(j in V where j < i)(i in INDEX_SET_EE) then 1 else max(j in V where j < i /\ i in INDEX_SET_EE)(z[j,0]) endif) endif));

constraint forall(i in V)(sum(c in 1..nc)(x[i,c]) = 1);

constraint forall(i in INDEX_SET_E, c in 1..nc)(x[E[i,1],c] + x[E[i,2],c] <= u[c]);



solve minimize sum(c in 1..nc)(u[c]);




