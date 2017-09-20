int: n = 8;


array[INDEX_SET_x_1, INDEX_SET_x_2] of var bool: x;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;


constraint forall(i in 1..n)(sum(j in 1..n)(x[i,j]) <= 1);

constraint forall(j in 1..n)(sum(i in 1..n)(x[i,j]) <= 1);

constraint forall(k in floor(2 - n)..floor(n - 2))(sum(i in 1..n, j in 1..n where i - j = k)(x[i,j]) <= 1);

constraint forall(k in 3..floor(n + n - 1))(sum(i in 1..n, j in 1..n where i + j = k)(x[i,j]) <= 1);



var float: obj = sum(i in 1..n, j in 1..n)(x[i,j]);

solve maximize obj;




