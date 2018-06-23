enum PROD;

int: T;

array[int, int] of float: revenue;

array[int] of float: prodcost;

array[int] of float: invcost;

array[int] of float: time_penalty;

array[int] of float: rate;

array[int] of float: inv0;

array[int, int] of float: commit;

array[int, int] of float: market;

array[int] of float: avail_min;

array[int] of float: avail_max;


array[INDEX_SET_Make_1, INDEX_SET_Make_2] of var float: Make;

array[INDEX_SET_Inv_1, INDEX_SET_Inv_2] of var float: Inv;

array[INDEX_SET_Use1_1] of var float: Use1;

array[INDEX_SET_Use2_1] of var float: Use2;

array[INDEX_SET_Sell_1, INDEX_SET_Sell_2] of var float: Sell;

set of int: INDEX_SET_Inv_1 = PROD;

set of int: INDEX_SET_Inv_2 = 0..T;

set of int: INDEX_SET_Make_1 = PROD;

set of int: INDEX_SET_Make_2 = 1..T;

set of int: INDEX_SET_Sell_1 = PROD;

set of int: INDEX_SET_Sell_2 = 1..T;

set of int: INDEX_SET_Use1_1 = 1..T;

set of int: INDEX_SET_Use2_1 = 1..T;


constraint forall(p in INDEX_SET_Make_1, t in INDEX_SET_Make_2)(Make[p,t] >= 0);

constraint forall(p in INDEX_SET_Inv_1, t0 in INDEX_SET_Inv_2)(Inv[p,t0] >= 0);

constraint forall(t in INDEX_SET_Use1_1)(Use1[t] <= avail_min[t] /\ Use1[t] >= 0);

constraint forall(t in INDEX_SET_Use2_1)(Use2[t] <= avail_max[t] - avail_min[t] /\ Use2[t] >= 0);

constraint forall(p in INDEX_SET_Sell_1, t in INDEX_SET_Sell_2)(Sell[p,t] <= market[p,t] /\ Sell[p,t] >= commit[p,t]);

constraint forall(t in 1..T)(sum(p in PROD)((1/rate[p]) * Make[p,t]) = Use1[t] + Use2[t]);

constraint forall(p in PROD)(Inv[p,0] = inv0[p]);

constraint forall(p in PROD, t in 1..T)(Make[p,t] + Inv[p,t - 1] = Sell[p,t] + Inv[p,t]);



solve maximize sum(p in PROD, t in 1..T)((revenue[p,t] * Sell[p,t] - prodcost[p] * Make[p,t] - invcost[p] * Inv[p,t]) - sum(t in 1..T)(time_penalty[t] * Use2[t]));




