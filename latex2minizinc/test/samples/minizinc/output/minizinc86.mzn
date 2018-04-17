set of int: ROW = 1..maxr;

set of int: COL = 1..maxc;

set of int: SOLDIER = 1..nsoldier;

set of int: SOLDIER0 = 0..nsoldier;

int: nsoldier;

array[int] of int: heightx = array1d(SOLDIER0,[strawheight] ++ height);

int: strawheight;

int: maxc;

int: maxr;

array[int] of int: height;


var ROW: nrow;

var COL: ncol;

array[INDEX_SET_x_1, INDEX_SET_x_2] of var SOLDIER0: x;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;


include "alldifferent_except_0.mzn";

constraint forall(r in ROW, c in COL)((r > nrow -> x[r,c] = 0) /\ (c > ncol -> x[r,c] = 0));

constraint alldifferent_except_0([x[r,c] | r in ROW, c in COL]);

constraint sum(r in ROW, c in COL)(x[r,c] != 0) = nsoldier;

constraint forall(r1 in ROW, c in COL)(r1 in 1..nrow /\ c in 1..ncol /\ x[r1,c] = 0 -> exists(r2 in ROW)(r2 < r1 /\ heightx[x[r2,c]] > strawheight));

constraint forall(r in ROW, c in COL)((r <= nrow /\ c <= ncol /\ x[r,c] = 0) -> (if c < maxc then x[r,c + 1] != 0 else false endif \/ if c > 1 then x[r,c - 1] != 0 else false endif \/ if r < maxr then x[r + 1,c] != 0 else false endif \/ if r > 1 then x[r - 1,c] != 0 else false endif));



solve maximize nrow * ncol;




