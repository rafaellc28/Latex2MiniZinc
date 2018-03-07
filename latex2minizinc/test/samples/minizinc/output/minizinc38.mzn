set of int: DIFF = 1..floor(n - 1);

set of int: NOTE = 1..n;

set of int: POSN = 1..n;

set of int: PDIFF = 1..floor(n - 1);

int: n;


array[INDEX_SET_posn_1] of var POSN: posn;

array[INDEX_SET_order_1] of var NOTE: order;

array[INDEX_SET_diffs_1] of var DIFF: diffs;

array[INDEX_SET_dposn_1] of var PDIFF: dposn;

set of int: INDEX_SET_diffs_1;

set of int: INDEX_SET_dposn_1;

set of int: INDEX_SET_order_1;

set of int: INDEX_SET_posn_1;


include "inverse.mzn";

constraint inverse(posn,order);

constraint forall(i in DIFF)(diffs[i] = abs(order[i] - order[i + 1]));

constraint inverse(diffs,dposn);

constraint abs(posn[1] - posn[n]) = 1;

constraint dposn[n - 1] = min(posn[1],posn[n]);

solve satisfy;


