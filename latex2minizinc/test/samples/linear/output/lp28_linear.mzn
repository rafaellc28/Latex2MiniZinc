enum PROD;

array[INDEX_SET_AREA] of set of int: AREA;

int: T;

array[int, int, int] of float: revenue;

array[int, int, int] of float: Sell;

array[int] of float: prodcost;

array[int, int] of float: Make;

array[int] of float: invcost;

array[int, int] of float: Inv;

array[int] of float: rate;

array[int] of float: avail;

array[int] of float: inv0;

array[int, int, int] of float: market;

set of int: INDEX_SET_AREA;


constraint forall(t in 1..T)(sum(p in PROD)((1/rate[p]) * Make[p,t]) <= avail[t]);

constraint forall(p in PROD)(Inv[p,0] = inv0[p]);

constraint forall(p in PROD, t in 1..T)(Make[p,t] + Inv[p,t - 1] = sum(a in AREA[p])(Sell[p,a,t] + Inv[p,t]));



solve maximize sum(p in PROD, t in 1..T)((sum(a in AREA[p])(revenue[p,a,t] * Sell[p,a,t] - prodcost[p] * Make[p,t] - invcost[p] * Inv[p,t])));




