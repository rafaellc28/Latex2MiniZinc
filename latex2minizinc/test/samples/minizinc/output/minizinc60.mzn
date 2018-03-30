set of int: DIG = 1..n;

set of int: POS = 1..l;

set of int: COPY = 1..m;

set of int: DIGCOP = 1..l;

int: m;

int: n;

int: l = m * n;


array[INDEX_SET_dc_1] of var DIGCOP: dc;

set of int: INDEX_SET_dc_1;


include "alldifferent.mzn";

constraint forall(d in DIG, c in 1..floor(m - 1), p in POS)(dc[p] = m * (d - 1) + c <-> dc[p + d + 1] = m * (d - 1) + c + 1);

constraint alldifferent([dc[p] | p in POS]);

solve satisfy;


