enum FOOD;

enum NUTR;

array[FOOD] of float: cost;

array[NUTR] of float: n_min;

array[NUTR, FOOD] of float: amt;

array[NUTR] of float: n_max;

array[FOOD] of float: f_min;

array[FOOD] of float: f_max;


array[FOOD] of var int: Buy;


constraint forall(f in FOOD)(assert(cost[f] > 0, "Assertion cost[\(f)] > 0 failed!"));

constraint forall(n in NUTR)(assert(n_min[n] >= 0, "Assertion n_min[\(n)] >= 0 failed!"));

constraint forall(n in NUTR, f in FOOD)(assert(amt[n,f] >= 0, "Assertion amt[\(n),\(f)] >= 0 failed!"));

constraint forall(n in NUTR)(assert(n_max[n] >= n_min[n], "Assertion n_max[\(n)] >= n_min[\(n)] failed!"));

constraint forall(f in FOOD)(assert(f_min[f] >= 0, "Assertion f_min[\(f)] >= 0 failed!"));

constraint forall(f in FOOD)(assert(f_max[f] >= f_min[f], "Assertion f_max[\(f)] >= f_min[\(f)] failed!"));

constraint forall(f in FOOD)(Buy[f] <= f_max[f] /\ Buy[f] >= f_min[f]);

constraint forall(i in NUTR)(sum(j in FOOD)(amt[i,j] * Buy[j]) <= n_max[i] /\ sum(j in FOOD)(amt[i,j] * Buy[j]) >= n_min[i]);



solve minimize sum(j in FOOD)(cost[j] * Buy[j]);




