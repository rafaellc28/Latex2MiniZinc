enum ACT;

enum PROD;

array[ACT] of float: cost;

array[PROD, ACT] of float: io;

array[PROD] of float: demand;


array[ACT] of var float: Level;


constraint forall(a in ACT)(assert(cost[a] > 0, "Assertion cost[\(a)] > 0 failed!"));

constraint forall(p in PROD, a in ACT)(assert(io[p,a] >= 0, "Assertion io[\(p),\(a)] >= 0 failed!"));

constraint forall(p in PROD)(assert(demand[p] >= 0, "Assertion demand[\(p)] >= 0 failed!"));

constraint forall(j in ACT)(Level[j] >= 0);

constraint forall(i in PROD)(sum(j in ACT)(io[i,j] * Level[j]) >= demand[i]);



solve minimize sum(j in ACT)(cost[j] * Level[j]);




