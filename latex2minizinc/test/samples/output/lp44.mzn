array[1..9, 1..9] of float: Givens;


array[1..9, 1..9, 1..9] of var bool: x;


constraint forall(i in 1..9, j in 1..9, k in 1..9 where Givens[i,j] != 0)(x[i,j,k] = if Givens[i,j] = k then 1 else 0 endif);

constraint forall(i1 in 1..9, j1 in 1..9, k in 1..9 where (i1-1) mod 3 = 0 /\ (j1-1) mod 3 = 0)(sum(i in i1..floor(i1 + 2), j in j1..floor(j1 + 2))(x[i,j,k]) = 1);

constraint forall(i in 1..9, j in 1..9)(sum(k in 1..9)(x[i,j,k]) = 1);

constraint forall(i in 1..9, k in 1..9)(sum(j in 1..9)(x[i,j,k]) = 1);

constraint forall(j in 1..9, k in 1..9)(sum(i in 1..9)(x[i,j,k]) = 1);

solve satisfy;


