set of int: PDIFF = 1..floor(n - 1);

set of int: NOTE = 1..n;

set of int: POSN = 1..n;

set of int: DIFF = 1..floor(n - 1);

int: n;


array[POSN] of var NOTE: order;

array[PDIFF] of var DIFF: diffs;


include "alldifferent.mzn";

constraint alldifferent(diffs);

constraint alldifferent(order);

constraint forall(i in PDIFF)(diffs[i] = abs(order[i] - order[i + 1]));

solve satisfy;


