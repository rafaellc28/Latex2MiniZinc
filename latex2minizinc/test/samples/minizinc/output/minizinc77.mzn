enum PRISONER;

set of PRISONER: female;

set of PRISONER: male = PRISONER diff female;

set of PRISONER: danger;

set of int: ROW = 1..n;

set of int: COL = 1..m;

int: m;

int: n;

array[ROW, COL] of int: cost;


var int: tCost = sum(p in PRISONER)(cost[r[p],c[p]]);

array[PRISONER] of var ROW: r;

array[PRISONER] of var COL: c;


include "alldifferent.mzn";

constraint alldifferent([r[p] * m + c[p] | p in PRISONER]);

constraint forall(p in female)(r[to_enum(PRISONER,p)] <= (floor((n + 1)) div 2));

constraint forall(p in male)(r[to_enum(PRISONER,p)] > (floor((n + 1)) div 2));

constraint forall(d in danger, p in PRISONER where d != p)((abs(r[to_enum(PRISONER,d)] - r[p]) + abs(c[to_enum(PRISONER,d)] - c[p])) > 1);



solve minimize tCost;




