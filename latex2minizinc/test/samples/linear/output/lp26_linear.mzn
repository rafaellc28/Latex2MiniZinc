enum PROD;

int: T;

array[PROD, 1..T] of float: revenue;

array[PROD] of float: prodcost;

array[PROD] of float: invcost;

array[PROD] of float: rate;

array[1..T] of float: avail;

array[PROD] of float: inv0;

array[PROD, 1..T] of float: market;


array[PROD, 1..T] of var float: Make;

array[PROD, 0..T] of var float: Inv;

array[PROD, 1..T] of var float: Sell;


constraint assert(T > 0, "Assertion T > 0 failed!");

constraint forall(p in PROD, t in 1..T)(assert(revenue[p,t] >= 0, "Assertion revenue[\(p),\(t)] >= 0 failed!"));

constraint forall(p in PROD)(assert(prodcost[p] >= 0, "Assertion prodcost[\(p)] >= 0 failed!"));

constraint forall(p in PROD)(assert(invcost[p] >= 0, "Assertion invcost[\(p)] >= 0 failed!"));

constraint forall(p in PROD)(assert(rate[p] > 0, "Assertion rate[\(p)] > 0 failed!"));

constraint forall(t in 1..T)(assert(avail[t] >= 0, "Assertion avail[\(t)] >= 0 failed!"));

constraint forall(p in PROD)(assert(inv0[p] >= 0, "Assertion inv0[\(p)] >= 0 failed!"));

constraint forall(p in PROD, t in 1..T)(assert(market[p,t] >= 0, "Assertion market[\(p),\(t)] >= 0 failed!"));

constraint forall(p in PROD, t in 1..T)(Make[p,t] >= 0);

constraint forall(p in PROD, t0 in 0..T)(Inv[p,t0] >= 0);

constraint forall(p in PROD, t in 1..T)(Sell[p,t] <= market[p,t] /\ Sell[p,t] >= 0);

constraint forall(t in 1..T)(sum(p in PROD)((1/rate[p]) * Make[p,t]) <= avail[t]);

constraint forall(p in PROD)(Inv[p,0] = inv0[p]);

constraint forall(p in PROD, t in 1..T)(Make[p,t] + Inv[p,t - 1] = Sell[p,t] + Inv[p,t]);



solve maximize sum(p in PROD, t in 1..T)((revenue[p,t] * Sell[p,t] - prodcost[p] * Make[p,t] - invcost[p] * Inv[p,t]));




