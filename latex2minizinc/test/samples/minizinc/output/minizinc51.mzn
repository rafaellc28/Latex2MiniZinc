set of int: BLOCK = 1..n;

set of int: ROFF = 1..m;

array[BLOCK, ROT] of set of ROFF: shape;

set of int: ROT = 1..4;

array[ROFF, 1..4] of int: d;

int: h;

int: n;

int: m;

array[ROFF, 1..2] of int: rsize = array2d(ROFF,1..2,[d[i,j] | i in ROFF, j in 3..4]);

array[ROFF, 1..2] of int: roff = array2d(ROFF,1..2,[d[i,j] | i in ROFF, j in 1..2]);

int: maxl;


array[BLOCK] of var 0..maxl: x;

var 0..maxl: l;

array[BLOCK] of var 0..h: y;

array[BLOCK] of var ROT: rot;


constraint forall(i in BLOCK)(shape[i,rot[i]] != {});

constraint forall(i in BLOCK)(forall(r in ROFF)(r in shape[i,rot[i]] -> (x[i] + d[r,1] + d[r,3] <= l /\ y[i] + d[r,2] + d[r,4] <= h)));

constraint forall(i,j in BLOCK where i < j)(forall(r1,r2 in ROFF)(r1 in shape[i,rot[i]] /\ r2 in shape[j,rot[j]] -> (x[i] + d[r1,1] + d[r1,3] <= x[j] + d[r2,1] \/ x[j] + d[r2,1] + d[r2,3] <= x[i] + d[r1,1] \/ y[i] + d[r1,2] + d[r1,4] <= y[j] + d[r2,2] \/ y[j] + d[r2,2] + d[r2,4] <= y[i] + d[r1,2])));



solve minimize l;




