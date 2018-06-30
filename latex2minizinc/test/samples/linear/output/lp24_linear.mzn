enum PROD;

int: T;

array[int, int] of float: revenue;

array[int, int] of float: commit;

array[int] of float: prodcost;

array[int] of float: invcost;

array[int] of float: time_penalty;

array[int] of float: rate;

array[int] of float: inv0;

array[int, int] of float: market;

array[int] of float: avail_min;

array[int] of float: avail_max;


array[INDEX_SET_Make_1, INDEX_SET_Make_2] of var float: Make;

array[INDEX_SET_Inv_1, INDEX_SET_Inv_2] of var float: Inv;

array[INDEX_SET_Use1_1] of var float: Use1;

array[INDEX_SET_Use2_1] of var float: Use2;

array[INDEX_SET_Sell1_1, INDEX_SET_Sell1_2] of var float: Sell1;

array[INDEX_SET_Sell0_1, INDEX_SET_Sell0_2] of var float: Sell0;

set of int: INDEX_SET_Inv_1 = PROD;

set of int: INDEX_SET_Inv_2 = 0..T;

set of int: INDEX_SET_Make_1 = PROD;

set of int: INDEX_SET_Make_2 = 1..T;

set of int: INDEX_SET_Sell0_1 = PROD;

set of int: INDEX_SET_Sell0_2 = 1..T;

set of int: INDEX_SET_Sell1_1 = PROD;

set of int: INDEX_SET_Sell1_2 = 1..T;

set of int: INDEX_SET_Use1_1 = 1..T;

set of int: INDEX_SET_Use2_1 = 1..T;


constraint forall(p in PROD, t in 1..T)(assert(revenue[p,t] >= 0, "Assertion revenue[\(p),\(t)] >= 0 failed!"));

constraint forall(p in PROD, t in 1..T)(assert(commit[p,t] >= 0, "Assertion commit[\(p),\(t)] >= 0 failed!"));

constraint forall(p in PROD)(assert(prodcost[p] >= 0, "Assertion prodcost[\(p)] >= 0 failed!"));

constraint forall(p in PROD)(assert(invcost[p] >= 0, "Assertion invcost[\(p)] >= 0 failed!"));

constraint forall(p in PROD)(assert(inv0[p] >= 0, "Assertion inv0[\(p)] >= 0 failed!"));

constraint forall(p in PROD, t in 1..T)(assert(market[p,t] >= 0, "Assertion market[\(p),\(t)] >= 0 failed!"));

constraint forall(t in 1..T)(assert(avail_min[t] >= 0, "Assertion avail_min[\(t)] >= 0 failed!"));

constraint forall(t in 1..T)(assert(avail_max[t] >= avail_min[t], "Assertion avail_max[\(t)] >= avail_min[t] failed!"));

constraint forall(p in INDEX_SET_Make_1, t in INDEX_SET_Make_2)(Make[p,t] >= 0);

constraint forall(p in INDEX_SET_Inv_1, t0 in INDEX_SET_Inv_2)(Inv[p,t0] >= 0);

constraint forall(t in INDEX_SET_Use1_1)(Use1[t] <= avail_min[t] /\ Use1[t] >= 0);

constraint forall(t in INDEX_SET_Use2_1)(Use2[t] <= avail_max[t] - avail_min[t] /\ Use2[t] >= 0);

constraint forall(p in INDEX_SET_Sell1_1, t in INDEX_SET_Sell1_2)(Sell1[p,t] <= market[p,t] - commit[p,t] /\ Sell1[p,t] >= 0);

constraint forall(p in INDEX_SET_Sell0_1, t in INDEX_SET_Sell0_2)(Sell0[p,t] <= commit[p,t] /\ Sell0[p,t] >= 0);

constraint forall(t in 1..T)(sum(p in PROD)((1/rate[p]) * Make[p,t]) = Use1[t] + Use2[t]);

constraint forall(p in PROD)(Inv[p,0] = inv0[p]);

constraint forall(p in PROD, t in 1..T)(Make[p,t] + Inv[p,t - 1] = (commit[p,t] + Sell1[p,t] - Sell0[p,t]) + Inv[p,t]);



solve maximize sum(p in PROD, t in 1..T)((revenue[p,t] * (commit[p,t] + Sell1[p,t] - Sell0[p,t]) - prodcost[p] * Make[p,t] - invcost[p] * Inv[p,t]) - sum(t in 1..T)(time_penalty[t] * Use2[t] - sum(p in PROD, t in 1..T)(1000000 * Sell0[p,t])));




