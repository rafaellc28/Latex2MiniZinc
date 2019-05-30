set of int: N = 1..n;

int: n;


array[INDEX_SET_t_1, INDEX_SET_t_2] of var bool: t;

set of int: INDEX_SET_t_1 = N;

set of int: INDEX_SET_t_2 = N;


include "lex_lesseq.mzn";

constraint sum(i,j in N)(t[i,j]) = n;

constraint forall(i in N)(sum(j in N)(t[i,j]) <= 1);

constraint forall(j in N)(sum(i in N)(t[i,j]) <= 1);

constraint forall(k in floor(1 - n)..floor(n - 1))(sum(i,j in N where i - j = k)(t[i,j]) <= 1);

constraint forall(k in 2..floor(2 * n))(sum(i,j in N where i + j = k)(t[i,j]) <= 1);

constraint let {array[N, N] of var bool: s} in
	(forall(i,j in N)(s[i,j] = t[j,n + 1 - i])) /\ lex_lesseq(array1d(t),array1d(s));

constraint let {array[N, N] of var bool: s} in
	(forall(i,j in N)(s[i,j] = t[n + 1 - i,n + 1 - j])) /\ lex_lesseq(array1d(t),array1d(s));

constraint let {array[N, N] of var bool: s} in
	(forall(i,j in N)(s[i,j] = t[n + 1 - j,i])) /\ lex_lesseq(array1d(t),array1d(s));

constraint let {array[N, N] of var bool: s} in
	(forall(i,j in N)(s[i,j] = t[n + 1 - i,j])) /\ lex_lesseq(array1d(t),array1d(s));

constraint let {array[N, N] of var bool: s} in
	(forall(i,j in N)(s[i,j] = t[i,n + 1 - j])) /\ lex_lesseq(array1d(t),array1d(s));

constraint let {array[N, N] of var bool: s} in
	(forall(i,j in N)(s[i,j] = t[n + 1 - j,n + 1 - i])) /\ lex_lesseq(array1d(t),array1d(s));

constraint let {array[N, N] of var bool: s} in
	(forall(i,j in N)(s[i,j] = t[j,i])) /\ lex_lesseq(array1d(t),array1d(s));

solve satisfy;


