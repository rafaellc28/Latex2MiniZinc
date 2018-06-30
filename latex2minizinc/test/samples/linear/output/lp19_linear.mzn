enum PROD;

enum STAGE;

array[int] of float: profit;

array[int, int] of float: rate;

array[int] of float: avail;

array[int] of float: commit;

array[int] of float: market;


array[INDEX_SET_Make_1] of var float: Make;

set of int: INDEX_SET_Make_1 = PROD;


constraint forall(s in STAGE)(assert(avail[s] >= 0, "Assertion avail[\(s)] >= 0 failed!"));

constraint forall(p in PROD)(assert(commit[p] >= 0, "Assertion commit[\(p)] >= 0 failed!"));

constraint forall(p in PROD)(assert(market[p] >= 0, "Assertion market[\(p)] >= 0 failed!"));

constraint forall(p in INDEX_SET_Make_1)(Make[p] <= market[p] /\ Make[p] >= commit[p]);

constraint forall(s in STAGE)(sum(p in PROD)((1/rate[p,s]) * Make[p]) <= avail[s]);



solve maximize sum(p in PROD)(profit[p] * Make[p]);




