enum FOOD;

set of int: MINREQ;

set of int: MAXREQ;

set of int: NUTR = MINREQ union MAXREQ;

array[FOOD] of float: cost;

array[NUTR, FOOD] of float: amt;

array[MINREQ] of float: n_min;

array[MAXREQ] of float: n_max;

array[FOOD] of float: f_min;

array[FOOD] of float: f_max;


array[FOOD] of var float: Buy;


constraint forall(f in FOOD)(assert(cost[f] > 0, "Assertion cost[\(f)] > 0 failed!"));

constraint forall(n in NUTR, f in FOOD)(assert(amt[n,f] >= 0, "Assertion amt[\(n),\(f)] >= 0 failed!"));

constraint forall(i in MINREQ)(assert(n_min[i] >= 0, "Assertion n_min[\(i)] >= 0 failed!"));

constraint forall(i in MAXREQ)(assert(n_max[i] >= n_min[i], "Assertion n_max[\(i)] >= n_min[\(i)] failed!"));

constraint forall(f in FOOD)(assert(f_min[f] >= 0, "Assertion f_min[\(f)] >= 0 failed!"));

constraint forall(f in FOOD)(assert(f_max[f] >= f_min[f], "Assertion f_max[\(f)] >= f_min[\(f)] failed!"));

constraint forall(f in FOOD)(Buy[f] <= f_max[f] /\ Buy[f] >= f_min[f]);

constraint forall(i in MINREQ)(sum(j in FOOD)(amt[i,j] * Buy[j]) >= n_min[i]);

constraint forall(i in MAXREQ)(sum(j in FOOD)(amt[i,j] * Buy[j]) <= n_max[i]);



solve minimize sum(j in FOOD)(cost[j] * Buy[j]);




