enum PROD;

int: T;

array[int, int] of float: revenue;

array[int] of float: prodcost;

array[int] of float: invcost;

array[int] of float: rate;

array[int] of float: avail;

array[int] of float: inv0;

array[int, int] of float: market;


array[INDEX_SET_Make_1, INDEX_SET_Make_2] of var float: Make;

array[INDEX_SET_Inv_1, INDEX_SET_Inv_2] of var float: Inv;

array[INDEX_SET_Sell_1, INDEX_SET_Sell_2] of var float: Sell;

set of int: INDEX_SET_Inv_1;

set of int: INDEX_SET_Inv_2 = 0..T;

set of int: INDEX_SET_Make_1;

set of int: INDEX_SET_Make_2 = 1..T;

set of int: INDEX_SET_Sell_1;

set of int: INDEX_SET_Sell_2 = 1..T;


constraint forall(p in PROD, t in INDEX_SET_Make_2)(Make[p,t] >= 0);

constraint forall(p in PROD, t0 in INDEX_SET_Inv_2)(Inv[p,t0] >= 0);

constraint forall(p in PROD, t in INDEX_SET_Sell_2)(Sell[p,t] <= market[p,t] /\ Sell[p,t] >= 0);

constraint forall(t in 1..T)(sum(p in PROD)((1/rate[p]) * Make[p,t]) <= avail[t]);

constraint forall(p in PROD)(Inv[p,0] = inv0[p]);

constraint forall(p in PROD, t in 1..T)(Make[p,t] + Inv[p,t - 1] = Sell[p,t] + Inv[p,t]);



solve maximize sum(p in PROD, t in 1..T)((revenue[p,t] * Sell[p,t] - prodcost[p] * Make[p,t] - invcost[p] * Inv[p,t]));




