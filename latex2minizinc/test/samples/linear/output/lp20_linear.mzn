enum PROD;

enum STAGE;

array[PROD] of float: profit;

array[PROD, STAGE] of float: rate;

array[STAGE] of float: avail = array1d(STAGE, [max(Normal(avail_mean[s],avail_variance[s]),0) | s in STAGE]);

array[PROD] of float: commit;

array[PROD] of float: market;

array[STAGE] of float: avail_mean;

array[STAGE] of float: avail_variance;


array[PROD] of var float: Make;


constraint forall(p in PROD, s in STAGE)(assert(rate[p,s] > 0, "Assertion rate[\(p),\(s)] > 0 failed!"));

constraint forall(p in PROD)(assert(commit[p] >= 0, "Assertion commit[\(p)] >= 0 failed!"));

constraint forall(p in PROD)(assert(market[p] >= 0, "Assertion market[\(p)] >= 0 failed!"));

constraint forall(s in STAGE)(assert(avail_mean[s] > 0, "Assertion avail_mean[\(s)] > 0 failed!"));

constraint forall(s in STAGE)(assert(avail_variance[s] < avail_mean[s]/(2 * avail[s]) /\ avail_variance[s] > 0, "Assertion avail_variance[\(s)] < avail_mean[\(s)]/(2 * avail[\(s)]) /\\ avail_variance[\(s)] > 0 failed!"));

constraint forall(p in PROD)(Make[p] <= market[p] /\ Make[p] >= commit[p]);

constraint forall(s in STAGE)(sum(p in PROD)((1/rate[p,s]) * Make[p]) <= avail[s]);



solve maximize sum(p in PROD)(profit[p] * Make[p]);




