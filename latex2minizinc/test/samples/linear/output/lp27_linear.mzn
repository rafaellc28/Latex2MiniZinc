enum PROD;

int: T;

array[int, int] of float: profit;

array[int] of float: rate;

array[int] of float: avail;

array[int, int] of float: market;


array[INDEX_SET_Make_1, INDEX_SET_Make_2] of var float: Make;

set of int: INDEX_SET_Make_1 = PROD;

set of int: INDEX_SET_Make_2 = 1..T;


constraint forall(t in 1..T)(assert(avail[t] >= 0, "Assertion avail[\(t)] >= 0 failed!"));

constraint forall(p in PROD, t in 1..T)(assert(market[p,t] >= 0, "Assertion market[\(p),\(t)] >= 0 failed!"));

constraint forall(p in INDEX_SET_Make_1, t in INDEX_SET_Make_2)(Make[p,t] <= market[p,t] /\ Make[p,t] >= 0);

constraint forall(t in 1..T)(sum(p in PROD)((1/rate[p]) * Make[p,t]) <= avail[t]);



solve maximize sum(p in PROD, t in 1..T)(profit[p,t] * Make[p,t]);




