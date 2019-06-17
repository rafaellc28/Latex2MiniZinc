enum PRODUCT;

enum RESOURCE;

array[PRODUCT, RESOURCE] of float: consumption;

array[RESOURCE] of float: capacity;

array[PRODUCT] of float: profit;


array[PRODUCT] of var int: produce;


constraint forall(p in PRODUCT)(produce[p] >= 0);

constraint forall(r in RESOURCE)(sum(p in PRODUCT)(consumption[p,r] * produce[p]) <= capacity[r]);



solve maximize sum(p in PRODUCT)(profit[p] * produce[p]);




