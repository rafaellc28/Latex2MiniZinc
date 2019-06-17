enum PRODUCT;

enum RESOURCE;

array[PRODUCT] of float: profit;

array[RESOURCE] of float: capacity;

array[PRODUCT, RESOURCE] of float: consumption;


array[PRODUCT] of var int: produce;


constraint forall(p in PRODUCT)(assert(profit[p] >= 0,"profit[\(p)] < 0!"));

constraint forall(r in RESOURCE)(assert(capacity[r] >= 0,"capacity[\(r)] < 0!"));

constraint forall(p in PRODUCT, r in RESOURCE)(assert(consumption[p,r] >= 0,"consumption[\(p),\(r)] < 0!"));

constraint forall(p in PRODUCT)(produce[p] >= 0);

constraint forall(r in RESOURCE)(sum(p in PRODUCT)(consumption[p,r] * produce[p]) <= capacity[r]);



solve maximize sum(p in PRODUCT)(profit[p] * produce[p]);




