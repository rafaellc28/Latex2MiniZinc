int: n = 8;


array[1..n, 1..n] of var bool: x;


constraint forall(i in 1..n)(sum(j in 1..n)(x[i,j]) <= 1);

constraint forall(j in 1..n)(sum(i in 1..n)(x[i,j]) <= 1);

constraint forall(k in floor(2 - n)..floor(n - 2))(sum(i in 1..n, j in 1..n where i - j = k)(x[i,j]) <= 1);

constraint forall(k in 3..floor(n + n - 1))(sum(i in 1..n, j in 1..n where i + j = k)(x[i,j]) <= 1);



solve maximize sum(i in 1..n, j in 1..n)(x[i,j]);




