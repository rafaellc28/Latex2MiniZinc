enum CUSTOMERS;

enum SOURCES;

array[int, int] of float: Tcost;

array[int] of float: Supply;

array[int] of float: Demand;


array[INDEX_SET_x_1, INDEX_SET_x_2] of var float: x;

set of int: INDEX_SET_x_1 = CUSTOMERS;

set of int: INDEX_SET_x_2 = SOURCES;


constraint forall(s in SOURCES)(assert(Supply[s] >= 0, "Assertion Supply[\(s)] >= 0 failed!"));

constraint forall(c in CUSTOMERS)(assert(Demand[c] >= 0, "Assertion Demand[\(c)] >= 0 failed!"));

constraint forall(c in INDEX_SET_x_1, s in INDEX_SET_x_2)(x[c,s] >= 0);

constraint forall(s in SOURCES)(sum(c in CUSTOMERS)(x[c,s]) <= Supply[s]);

constraint forall(c in CUSTOMERS)(sum(s in SOURCES)(x[c,s]) = Demand[c]);



solve minimize sum(c in CUSTOMERS, s in SOURCES)(Tcost[c,s] * x[c,s]);




