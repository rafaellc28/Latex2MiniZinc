enum FOOD;

enum STORE;

set of int: MINREQ;

set of int: MAXREQ;

set of int: NUTR = MINREQ union MAXREQ;

float: lambda = 0.85;

array[STORE, FOOD] of float: cost;

array[NUTR, FOOD] of float: amt;

array[MINREQ] of float: n_min;

array[MAXREQ] of float: n_max;

array[FOOD] of float: f_min;

array[FOOD] of float: f_max;


array[FOOD] of var float: Buy;


constraint forall(s in STORE, f in FOOD)(assert(cost[s,f] > 0, "Assertion cost[\(s),\(f)] > 0 failed!"));

constraint forall(n in NUTR, f in FOOD)(assert(amt[n,f] >= 0, "Assertion amt[\(n),\(f)] >= 0 failed!"));

constraint forall(mi in MINREQ)(assert(n_min[mi] >= 0, "Assertion n_min[\(mi)] >= 0 failed!"));

constraint forall(ma in MAXREQ)(assert(n_max[ma] >= 0, "Assertion n_max[\(ma)] >= 0 failed!"));

constraint forall(f in FOOD)(assert(f_min[f] >= 0, "Assertion f_min[\(f)] >= 0 failed!"));

constraint forall(j in FOOD)(Buy[j] <= f_max[j] /\ Buy[j] >= f_min[j]);

constraint forall(i in MINREQ)(sum(j in FOOD)(amt[i,j] * Buy[j]) >= n_min[i]);

constraint forall(i in MAXREQ)(sum(j in FOOD)(amt[i,j] * Buy[j]) <= n_max[i]);



solve minimize lambda * (sum(j in FOOD)(Buy[j])) + (1 - lambda) * (sum(s in STORE)(sum(j in FOOD)(cost[s,j] * Buy[j])));




