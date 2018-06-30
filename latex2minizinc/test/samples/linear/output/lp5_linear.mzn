enum ACT;

enum PROD;

array[int] of float: cost;

array[int] of float: Level;

array[int, int] of float: io;

array[int] of float: demand;

array[int] of float: level_min;

array[int] of float: level_max;


constraint forall(j in ACT)(assert(Level[j] <= level_max[j] /\ Level[j] >= level_min[j], "Assertion Level[\(j)] <= level_max[j]Level[\(j)] >= level_min[j] failed!"));

constraint forall(p in PROD, a in ACT)(assert(io[p,a] >= 0, "Assertion io[\(p),\(a)] >= 0 failed!"));

constraint forall(p in PROD)(assert(demand[p] >= 0, "Assertion demand[\(p)] >= 0 failed!"));

constraint forall(i in PROD)(sum(j in ACT)(io[i,j] * Level[j]) >= demand[i]);



solve minimize sum(j in ACT)(cost[j] * Level[j]);




