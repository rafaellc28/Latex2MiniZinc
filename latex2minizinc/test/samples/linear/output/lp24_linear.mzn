enum PROD;

int: T;

array[PROD, 1..T] of float: revenue;

array[PROD, 1..T] of float: commit;

array[PROD] of float: prodcost;

array[PROD] of float: invcost;

array[1..T] of float: time_penalty;

array[PROD] of float: rate;

array[PROD] of float: inv0;

array[PROD, 1..T] of float: market;

array[1..T] of float: avail_min;

array[1..T] of float: avail_max;


array[PROD, 1..T] of var float: Make;

array[PROD, 0..T] of var float: Inv;

array[1..T] of var float: Use1;

array[1..T] of var float: Use2;

array[PROD, 1..T] of var float: Sell1;

array[PROD, 1..T] of var float: Sell0;


constraint assert(T > 0, "Assertion T > 0 failed!");

constraint forall(p in PROD, t in 1..T)(assert(revenue[p,t] >= 0, "Assertion revenue[\(p),\(t)] >= 0 failed!"));

constraint forall(p in PROD, t in 1..T)(assert(commit[p,t] >= 0, "Assertion commit[\(p),\(t)] >= 0 failed!"));

constraint forall(p in PROD)(assert(prodcost[p] >= 0, "Assertion prodcost[\(p)] >= 0 failed!"));

constraint forall(p in PROD)(assert(invcost[p] >= 0, "Assertion invcost[\(p)] >= 0 failed!"));

constraint forall(t in 1..T)(assert(time_penalty[t] > 0, "Assertion time_penalty[\(t)] > 0 failed!"));

constraint forall(p in PROD)(assert(rate[p] > 0, "Assertion rate[\(p)] > 0 failed!"));

constraint forall(p in PROD)(assert(inv0[p] >= 0, "Assertion inv0[\(p)] >= 0 failed!"));

constraint forall(p in PROD, t in 1..T)(assert(market[p,t] >= 0, "Assertion market[\(p),\(t)] >= 0 failed!"));

constraint forall(t in 1..T)(assert(avail_min[t] >= 0, "Assertion avail_min[\(t)] >= 0 failed!"));

constraint forall(t in 1..T)(assert(avail_max[t] >= avail_min[t], "Assertion avail_max[\(t)] >= avail_min[\(t)] failed!"));

constraint forall(p in PROD, t in 1..T)(Make[p,t] >= 0);

constraint forall(p in PROD, t0 in 0..T)(Inv[p,t0] >= 0);

constraint forall(t in 1..T)(Use1[t] <= avail_min[t] /\ Use1[t] >= 0);

constraint forall(t in 1..T)(Use2[t] <= avail_max[t] - avail_min[t] /\ Use2[t] >= 0);

constraint forall(p in PROD, t in 1..T)(Sell1[p,t] <= market[p,t] - commit[p,t] /\ Sell1[p,t] >= 0);

constraint forall(p in PROD, t in 1..T)(Sell0[p,t] <= commit[p,t] /\ Sell0[p,t] >= 0);

constraint forall(t in 1..T)(sum(p in PROD)((1/rate[p]) * Make[p,t]) = Use1[t] + Use2[t]);

constraint forall(p in PROD)(Inv[p,0] = inv0[p]);

constraint forall(p in PROD, t in 1..T)(Make[p,t] + Inv[p,t - 1] = (commit[p,t] + Sell1[p,t] - Sell0[p,t]) + Inv[p,t]);



solve maximize sum(p in PROD, t in 1..T)((revenue[p,t] * (commit[p,t] + Sell1[p,t] - Sell0[p,t]) - prodcost[p] * Make[p,t] - invcost[p] * Inv[p,t]) - sum(t in 1..T)(time_penalty[t] * Use2[t] - sum(p in PROD, t in 1..T)(1000000 * Sell0[p,t])));




