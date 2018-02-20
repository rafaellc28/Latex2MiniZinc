enum PRODUCT;

enum RESOURCE;

array[int, int] of float: consumption;

array[int] of float: capacity;

array[int] of float: profit;


array[INDEX_SET_produce_1] of var int: produce;

set of int: INDEX_SET_produce_1;


constraint forall(p in PRODUCT)(produce[p] >= 0);

constraint forall(r in RESOURCE)(sum(p in PRODUCT)(consumption[p,r] * produce[p]) <= capacity[r]);



solve maximize sum(p in PRODUCT)(profit[p] * produce[p]);




