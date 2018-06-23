set of int: DIG = 1..n;

set of int: COPY = 1..m;

set of int: POS = 1..l;

int: m;

int: n;

int: l = m * n;


array[INDEX_SET_p_1, INDEX_SET_p_2] of var POS: p;

set of int: INDEX_SET_p_1 = DIG;

set of int: INDEX_SET_p_2 = COPY;


include "alldifferent.mzn";

constraint forall(d in DIG, c in 1..floor(m - 1))(p[d,c + 1] = p[d,c] + d + 1);

constraint alldifferent([p[d,c] | d in DIG, c in COPY]);

solve satisfy;


