enum V;

array[INDEX_SET_E, 1..2] of V: E;

int: Nc;


array[INDEX_SET_u_1] of var bool: u;

array[INDEX_SET_x_1, INDEX_SET_x_2] of var bool: x;

set of int: INDEX_SET_E;

set of int: INDEX_SET_u_1;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;


constraint forall(i in V)(sum(c in 1..Nc)(x[i,c]) = 1);

constraint forall(i in INDEX_SET_E, c in 1..Nc)(x[E[i,1],c] + x[E[i,2],c] <= u[c]);



var float: obj = sum(c in 1..Nc)(u[c]);

solve minimize obj;




