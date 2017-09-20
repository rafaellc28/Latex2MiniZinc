set of int: V = 1..n;

array[INDEX_SET_E, 1..2] of V: E;

array[INDEX_SET_EE, 1..2] of V: EE = array2d(INDEX_SET_EE, 1..2, [if idx2 == 1 then E[i,1] else E[i,2] endif | i in INDEX_SET_E, idx2 in 1..2]) union array2d(INDEX_SET_EE, 1..2, [if idx2 == 1 then E[i,2] else E[i,1] endif | i in INDEX_SET_E, idx2 in 1..2]);

int: nc = max(i in V)(z[i,0]);

int: n;

array[int, int] of int: z;


array[INDEX_SET_u_1] of var bool: u;

array[INDEX_SET_x_1, INDEX_SET_x_2] of var bool: x;

set of int: INDEX_SET_E;

set of int: INDEX_SET_EE;

set of int: INDEX_SET_u_1;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;


constraint forall(i in V, case in 0..1)(z[EE[i,1],case] = (if case = 0 then (min(c in 1..z[i,1])((if not exists(j in V where j < i /\ i in INDEX_SET_EE)(z[EE[i,2],0] = c) then c else z[EE[i,1],1] + 1 endif))) else (if not exists(j in V where j < i)(i in INDEX_SET_EE) then 1 else max(j in V where j < i /\ i in INDEX_SET_EE)(z[EE[i,2],0]) endif) endif));

constraint forall(i in V)(sum(c in 1..nc)(x[i,c]) = 1);

constraint forall(i in INDEX_SET_E, c in 1..nc)(x[E[i,1],c] + x[E[i,2],c] <= u[c]);



var float: obj = sum(c in 1..nc)(u[c]);

solve minimize obj;




