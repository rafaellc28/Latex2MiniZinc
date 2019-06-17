int: N;


array[1..N, 1..N] of var bool: x;


constraint forall(i in 1..N)(sum(j in 1..N)(x[i,j]) <= 1);

constraint forall(j in 1..N)(sum(i in 1..N)(x[i,j]) <= 1);

constraint forall(k in floor(2 - N)..floor(N - 2))(sum(i in 1..N, j in 1..N where i - j = k)(x[i,j]) <= 1);

constraint forall(k in 3..floor(N + N - 1))(sum(i in 1..N, j in 1..N where i + j = k)(x[i,j]) <= 1);



solve maximize sum(i in 1..N, j in 1..N)(x[i,j]);




