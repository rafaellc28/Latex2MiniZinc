enum PRISONER;

set of PRISONER: female;

set of PRISONER: male = PRISONER diff female;

set of PRISONER: danger;

set of int: ROW = 1..n;

set of int: COL = 1..m;

int: m;

int: n;

array[int, int] of int: cost;


var int: tCost = sum(p in PRISONER)(cost[r[p],c[p]]);

array[INDEX_SET_r_1] of var ROW: r;

array[INDEX_SET_c_1] of var COL: c;

set of int: INDEX_SET_c_1 = PRISONER;

set of int: INDEX_SET_r_1 = PRISONER;


include "alldifferent.mzn";

constraint alldifferent([r[p] * m + c[p] | p in PRISONER]);

constraint forall(p in female)(r[p] <= (floor((n + 1)) div 2));

constraint forall(p in male)(r[p] > (floor((n + 1)) div 2));

constraint forall(d in danger, p in PRISONER where d != p)((abs(r[d] - r[p]) + abs(c[d] - c[p])) > 1);



solve minimize tCost;




