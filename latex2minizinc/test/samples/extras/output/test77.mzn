enum PRODUCT;

enum RESOURCE;

array[PRODUCT, RESOURCE] of float: consumption;

array[RESOURCE] of float: capacity;

array[PRODUCT] of float: profit;


array[PRODUCT] of var int: produce;


constraint forall(p in PRODUCT, r in RESOURCE)(assert(consumption[p,r] >= 0, "Assertion consumption[\(p),\(r)] >= 0 failed!"));

constraint forall(r in RESOURCE)(assert(capacity[r] >= 0, "Assertion capacity[\(r)] >= 0 failed!"));

constraint forall(p in PRODUCT)(assert(profit[p] >= 0, "Assertion profit[\(p)] >= 0 failed!"));

constraint forall(p in PRODUCT)(produce[p] >= 0);

constraint forall(r in RESOURCE)(sum(p in PRODUCT)(consumption[p,r] * produce[p]) <= capacity[r]);



solve maximize sum(p in PRODUCT)(profit[p] * produce[p]);




