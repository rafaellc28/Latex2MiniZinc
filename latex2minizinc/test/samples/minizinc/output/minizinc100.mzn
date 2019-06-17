set of int: N = 1..n;

int: n;


array[N, N] of var bool: t;


constraint sum(i,j in N)(t[i,j]) = n;

constraint forall(i in N)(sum(j in N)(t[i,j]) <= 1);

constraint forall(j in N)(sum(i in N)(t[i,j]) <= 1);

constraint forall(k in floor(1 - n)..floor(n - 1))(sum(i,j in N where i - j = k)(t[i,j]) <= 1);

constraint forall(k in 2..floor(2 * n))(sum(i,j in N where i + j = k)(t[i,j]) <= 1);

include "rot_flip_sqr_sym.mzn";

constraint rot_flip_sqr_sym(t);

solve satisfy;


