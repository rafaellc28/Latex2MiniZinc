set of int: COL = 1..b;

set of int: ROW = 1..v;

int: r;

int: k;

int: lambda;

int: v;

int: b;


array[ROW, COL] of var bool: m;


include "lex_lesseq.mzn";

constraint forall(i in ROW)(sum(j in COL)(m[i,j]) = r);

constraint forall(j in COL)(sum(i in ROW)(m[i,j]) = k);

constraint forall(i1,i2 in ROW where i1 < i2)(sum(j in COL)(m[i1,j] = true /\ m[i2,j] = true) = lambda);

constraint forall(i in 1..floor(v - 1))(lex_lesseq([m[i,j] | j in COL],[m[i + 1,j] | j in COL]));

constraint forall(j in 1..floor(b - 1))(lex_lesseq([m[i,j] | i in ROW],[m[i,j + 1] | i in ROW]));

solve satisfy;


