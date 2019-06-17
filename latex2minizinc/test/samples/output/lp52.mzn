enum V;

array[INDEX_SET_E, 1..2] of V: E;

int: Nc;


array[1..Nc] of var bool: u;

array[V, 1..Nc] of var bool: x;

set of int: INDEX_SET_E;


constraint forall(i in V)(sum(c in 1..Nc)(x[i,c]) = 1);

constraint forall(i in INDEX_SET_E, c in 1..Nc)(x[to_enum(V,E[i,1]),c] + x[to_enum(V,E[i,2]),c] <= u[c]);



solve minimize sum(c in 1..Nc)(u[c]);




