set of int: COL = 1..b;

set of int: ROW = 1..v;

int: r;

int: k;

int: lambda;

int: v;

int: b;


array[INDEX_SET_m_1, INDEX_SET_m_2] of var bool: m;

set of int: INDEX_SET_m_1;

set of int: INDEX_SET_m_2;


include "lex_lesseq.mzn";

constraint forall(i in ROW)(sum(j in COL)(m[i,j]) = r);

constraint forall(j in COL)(sum(i in ROW)(m[i,j]) = k);

constraint forall(i1,i2 in ROW where i1 < i2)(sum(j in COL)(m[i1,j] = true /\ m[i2,j] = true) = lambda);

constraint forall(i in 1..floor(v - 1))(lex_lesseq(row(m,i),row(m,i + 1)));

constraint forall(j in 1..floor(b - 1))(lex_lesseq(col(m,j),col(m,j + 1)));

solve satisfy;


