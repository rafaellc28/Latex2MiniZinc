enum PROD;

int: T;

array[PROD, 1..T] of float: profit;

array[PROD] of float: rate;

array[1..T] of float: avail;

array[PROD, 1..T] of float: market;


array[PROD, 1..T] of var float: Make;


constraint assert(T > 0, "Assertion T > 0 failed!");

constraint forall(p in PROD)(assert(rate[p] > 0, "Assertion rate[\(p)] > 0 failed!"));

constraint forall(t in 1..T)(assert(avail[t] >= 0, "Assertion avail[\(t)] >= 0 failed!"));

constraint forall(p in PROD, t in 1..T)(assert(market[p,t] >= 0, "Assertion market[\(p),\(t)] >= 0 failed!"));

constraint forall(p in PROD, t in 1..T)(Make[p,t] <= market[p,t] /\ Make[p,t] >= 0);

constraint forall(t in 1..T)(sum(p in PROD)((1/rate[p]) * Make[p,t]) <= avail[t]);



solve maximize sum(p in PROD, t in 1..T)(profit[p,t] * Make[p,t]);




