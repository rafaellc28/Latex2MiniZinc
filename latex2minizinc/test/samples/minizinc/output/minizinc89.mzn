set of int: ROW = 1..maxr;

set of int: COL = 1..maxc;

set of int: SOLDIER = 1..nsoldier;

set of int: SOLDIER0 = 0..nsoldier;

set of int: DIFF = 0..max(height);

int: nsoldier;

array[SOLDIER0] of int: heightx = array1d(SOLDIER0,[strawheight] ++ height);

int: strawheight;

int: maxc;

int: maxr;

array[SOLDIER] of int: height;


var ROW: nrow;

var COL: ncol;

array[ROW, COL] of var SOLDIER0: x;

array[ROW, COL] of var DIFF: hd;


include "global_cardinality_low_up.mzn";

include "alldifferent_except_0.mzn";

constraint forall(r in ROW, c in COL)((r > nrow -> x[r,c] = 0) /\ (c > ncol -> x[r,c] = 0));

constraint alldifferent_except_0([x[r,c] | r in ROW, c in COL]);

constraint sum(r in ROW, c in COL)(x[r,c] != 0) = nsoldier;

constraint forall(r1 in ROW, c in COL)(r1 in 1..nrow /\ c in 1..ncol /\ x[r1,c] = 0 -> exists(r2 in ROW)(r2 < r1 /\ heightx[x[r2,c]] > strawheight));

constraint forall(r in ROW, c in COL)((r <= nrow /\ c <= ncol /\ x[r,c] = 0) -> (if c < maxc then x[r,c + 1] != 0 else false endif \/ if c > 1 then x[r,c - 1] != 0 else false endif \/ if r < maxr then x[r + 1,c] != 0 else false endif \/ if r > 1 then x[r - 1,c] != 0 else false endif));

constraint forall(r in nrow + 1..maxr, c in ncol + 1..maxc)(x[r,c] = 0);

constraint forall(r in ROW, c in COL)((r > nrow -> x[r,c] = 0) /\ (c > ncol -> x[r,c] = 0));

constraint forall(r1,r2 in ROW, c1,c2 in COL where r1 != r2 \/ c1 != c2)(x[r1,c1] = 0 \/ x[r1,c1] != x[r2,c2]);

constraint forall(s in SOLDIER)(exists(r in ROW, c in COL)(r <= nrow /\ c <= ncol /\ x[r,c] = s));

constraint global_cardinality_low_up([x[r,c] | r in ROW, c in COL],[s | s in SOLDIER],[1 | s in SOLDIER],[1 | s in SOLDIER]);

constraint not exists(r1 in ROW, c in COL)(r1 in 1..nrow /\ c in 1..ncol /\ x[r1,c] = 0 /\ forall(r2 in ROW)(r2 < r1 -> (x[r2,c] = 0 \/ height[x[r2,c]] <= strawheight)));

constraint not exists(r1 in ROW, c in COL)((r1 in 1..nrow /\ c in 1..ncol /\ x[r1,c] = 0 /\ forall(r2 in ROW)((r2 < r1 -> heightx[x[r2,c]] <= strawheight))));

constraint forall(r in ROW)(forall(c in 1..ncol - 1)((if r > nrow \/ c > ncol then hd[r,c] = 0 else if x[r,c] = 0 then if x[r,c + 1] = 0 then hd[r,c] = 0 else hd[r,c] = abs(strawheight - height[x[r,c + 1]]) endif else if x[r,c + 1] = 0 then hd[r,c] = abs(height[x[r,c]] - strawheight) else hd[r,c] = abs(height[x[r,c]] - height[x[r,c + 1]]) endif endif endif)));

constraint forall(c in COL)(hd[nrow,c] = 0);



solve maximize nrow * ncol;




