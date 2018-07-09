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

set of int: INDEX_SET_Inv_1 = PROD;

set of int: INDEX_SET_Inv_2 = 0..T;

set of int: INDEX_SET_Make_1 = PROD;

set of int: INDEX_SET_Make_2 = 1..T;

set of int: INDEX_SET_Sell_1 = PROD;

set of int: INDEX_SET_Sell_2 = 1..T;


constraint assert(T > 0, "Assertion T > 0 failed!");

constraint forall(p in PROD, t in 1..T)(assert(revenue[p,t] >= 0, "Assertion revenue[\(p),\(t)] >= 0 failed!"));

constraint forall(p in PROD)(assert(prodcost[p] >= 0, "Assertion prodcost[\(p)] >= 0 failed!"));

constraint forall(p in PROD)(assert(invcost[p] >= 0, "Assertion invcost[\(p)] >= 0 failed!"));

constraint forall(p in PROD)(assert(rate[p] > 0, "Assertion rate[\(p)] > 0 failed!"));

constraint forall(t in 1..T)(assert(avail[t] >= 0, "Assertion avail[\(t)] >= 0 failed!"));

constraint forall(p in PROD)(assert(inv0[p] >= 0, "Assertion inv0[\(p)] >= 0 failed!"));

constraint forall(p in PROD, t in 1..T)(assert(market[p,t] >= 0, "Assertion market[\(p),\(t)] >= 0 failed!"));

constraint forall(p in INDEX_SET_Make_1, t in INDEX_SET_Make_2)(Make[p,t] >= 0);

constraint forall(p in INDEX_SET_Inv_1, t0 in INDEX_SET_Inv_2)(Inv[p,t0] >= 0);

constraint forall(p in INDEX_SET_Sell_1, t in INDEX_SET_Sell_2)(Sell[p,t] <= market[p,t] /\ Sell[p,t] >= 0);

constraint forall(t in 1..T)(sum(p in PROD)((1/rate[p]) * Make[p,t]) <= avail[t]);

constraint forall(p in PROD)(Inv[p,0] = inv0[p]);

constraint forall(p in PROD, t in 1..T)(Make[p,t] + Inv[p,t - 1] = Sell[p,t] + Inv[p,t]);



solve maximize sum(p in PROD, t in 1..T)((revenue[p,t] * Sell[p,t] - prodcost[p] * Make[p,t] - invcost[p] * Inv[p,t]));




