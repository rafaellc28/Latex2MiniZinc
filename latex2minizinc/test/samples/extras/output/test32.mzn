enum PROD;

float: avail;

array[PROD] of float: rate;

array[PROD] of float: Make;


constraint ((avail >= 0 \/ avail >= 2)) -> sum(p in PROD)((1/rate[p]) * Make[p]) <= avail;

solve satisfy;


