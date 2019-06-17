set of int: DIG = 1..n;

set of int: COPY = 1..m;

set of int: POS = 1..l;

set of int: DIGCOP = 1..l;

int: m;

int: n;

int: l = m * n;


array[DIG, COPY] of var POS: p;

array[POS] of var DIGCOP: dc;


include "inverse.mzn";

constraint forall(d in DIG, c in 1..floor(m - 1))(p[d,c + 1] = p[d,c] + d + 1);

constraint inverse(dc,[p[d,c] | d in DIG, c in COPY]);

solve satisfy;


