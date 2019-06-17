set of int: ROWS = 1..n;

set of int: COLUMNS = 1..n;

int: n;


array[ROWS, COLUMNS] of var bool: X;


constraint forall(j in COLUMNS)(sum(i in ROWS)(X[i,j]) = 1);

constraint forall(i in ROWS)(sum(j in COLUMNS)(X[i,j]) = 1);

constraint forall(k in 2..floor(2 * n))(sum(i in ROWS, j in COLUMNS where i + j = k)(X[i,j]) <= 1);

constraint forall(k in -(n - 1)..(n - 1))(sum(i in ROWS, j in COLUMNS where i - j = k)(X[i,j]) <= 1);

solve satisfy;


