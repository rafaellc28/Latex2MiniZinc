array[INDEX_SET_b_1] of var 0..1: b;

array[INDEX_SET_x_1] of var 1..100: x;

array[INDEX_SET_vlist_1] of var int: vlist = [b[i] | i in 1..15] ++ [x[i] | i in 1..4];

set of int: INDEX_SET_b_1 = 1..15;

set of int: INDEX_SET_vlist_1 = 1..19;

set of int: INDEX_SET_x_1 = 1..4;


include "alldifferent.mzn";

constraint sum(b) >= 1;

constraint alldifferent(x) /\ x[1] = x[2];

solve satisfy;


