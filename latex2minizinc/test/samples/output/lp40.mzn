enum N;

int: C;


array[INDEX_SET_x_1, INDEX_SET_x_2, INDEX_SET_x_3] of var bool: x;

var float: s;

set of int: INDEX_SET_x_1 = 1..C;

set of int: INDEX_SET_x_2 = 1..C;

set of int: INDEX_SET_x_3 = N;


constraint forall(i in 1..C, j in 1..C)(sum(k in N)(x[i,j,k]) = 1);

constraint forall(k in N)(sum(i in 1..C, j in 1..C)(x[i,j,k]) = 1);

constraint forall(i in 1..C)(sum(j in 1..C, k in N)(k * x[i,j,k]) = s);

constraint forall(j in 1..C)(sum(i in 1..C, k in N)(k * x[i,j,k]) = s);

constraint sum(i in 1..C, k in N)(k * x[i,i,k]) = s;

constraint sum(i in 1..C, k in N)(k * x[i,C - i + 1,k]) = s;

solve satisfy;


