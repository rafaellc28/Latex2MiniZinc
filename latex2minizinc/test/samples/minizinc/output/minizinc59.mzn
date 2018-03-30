set of int: DIG = 1..n;

set of int: COPY = 1..m;

set of int: POS = 1..l;

set of int: DIGCOP = 1..l;

int: m;

int: n;

int: l = m * n;


array[INDEX_SET_p_1, INDEX_SET_p_2] of var POS: p;

array[INDEX_SET_dc_1] of var DIGCOP: dc;

set of int: INDEX_SET_dc_1;

set of int: INDEX_SET_p_1;

set of int: INDEX_SET_p_2;


include "inverse.mzn";

constraint forall(d in DIG, c in 1..floor(m - 1))(p[d,c + 1] = p[d,c] + d + 1);

constraint inverse(dc,[p[d,c] | d in DIG, c in COPY]);

solve satisfy;


