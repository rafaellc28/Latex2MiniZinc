int: N;


array[INDEX_SET_x_1, INDEX_SET_x_2] of var bool: x;

set of int: INDEX_SET_x_1 = 1..N;

set of int: INDEX_SET_x_2 = 1..N;


constraint forall(i in 1..N)(sum(j in 1..N)(x[i,j]) <= 1);

constraint forall(j in 1..N)(sum(i in 1..N)(x[i,j]) <= 1);

constraint forall(k in floor(2 - N)..floor(N - 2))(sum(i in 1..N, j in 1..N where i - j = k)(x[i,j]) <= 1);

constraint forall(k in 3..floor(N + N - 1))(sum(i in 1..N, j in 1..N where i + j = k)(x[i,j]) <= 1);



var float: obj = sum(i in 1..N, j in 1..N)(x[i,j]);

solve maximize obj;




