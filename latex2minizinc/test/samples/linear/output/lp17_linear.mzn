enum PROD;

array[PROD] of float: profit;

array[PROD] of float: rate;

float: avail;

array[PROD] of float: market;


array[PROD] of var float: Make;


constraint forall(p in PROD)(assert(rate[p] > 0, "Assertion rate[\(p)] > 0 failed!"));

constraint assert(avail >= 0, "Assertion avail >= 0 failed!");

constraint forall(p in PROD)(assert(market[p] >= 0, "Assertion market[\(p)] >= 0 failed!"));

constraint forall(p in PROD)(Make[p] <= market[p] /\ Make[p] >= 0);

constraint sum(p in PROD)((1/rate[p]) * Make[p]) <= avail;



solve maximize sum(p in PROD)(profit[p] * Make[p]);




