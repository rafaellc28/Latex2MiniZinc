enum PROD;

float: avail;

array[PROD] of float: rate;

array[PROD] of float: market;


array[PROD] of var float: Make;


constraint forall(p in PROD)(Make[p] >= 0);

constraint forall(p in PROD)(Make[p] <= market[p]);

constraint avail > 0 -> sum(p in PROD)((1/rate[p]) * Make[p]) <= avail;

solve satisfy;


