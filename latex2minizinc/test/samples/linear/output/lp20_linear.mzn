enum PROD;

enum STAGE;

array[int] of float: profit;

array[int, int] of float: rate;

array[INDEX_SET_avail_1] of float: avail = array1d(INDEX_SET_avail_1, [max(Normal(avail_mean[s],avail_variance[s]),0) | s in STAGE]);

array[int] of float: commit;

array[int] of float: market;

array[int] of float: avail_mean;

array[int] of float: avail_variance;


array[INDEX_SET_Make_1] of var float: Make;

set of int: INDEX_SET_Make_1 = PROD;

set of int: INDEX_SET_avail_1;


constraint forall(p in PROD, s in STAGE)(assert(rate[p,s] > 0, "Assertion rate[\(p),\(s)] > 0 failed!"));

constraint forall(p in PROD)(assert(commit[p] >= 0, "Assertion commit[\(p)] >= 0 failed!"));

constraint forall(p in PROD)(assert(market[p] >= 0, "Assertion market[\(p)] >= 0 failed!"));

constraint forall(s in STAGE)(assert(avail_mean[s] > 0, "Assertion avail_mean[\(s)] > 0 failed!"));

constraint forall(s in STAGE)(assert(avail_variance[s] < avail_mean[s]/(2 * avail[s]) /\ avail_variance[s] > 0, "Assertion avail_variance[\(s)] < avail_mean[\(s)]/(2 * avail[\(s)]) /\\ avail_variance[\(s)] > 0 failed!"));

constraint forall(p in INDEX_SET_Make_1)(Make[p] <= market[p] /\ Make[p] >= commit[p]);

constraint forall(s in STAGE)(sum(p in PROD)((1/rate[p,s]) * Make[p]) <= avail[s]);



solve maximize sum(p in PROD)(profit[p] * Make[p]);




