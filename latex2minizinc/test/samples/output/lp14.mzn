enum CUSTOMERS;

enum SOURCES;

array[CUSTOMERS, SOURCES] of float: Tcost;

array[SOURCES] of float: Supply;

array[CUSTOMERS] of float: Demand;


array[CUSTOMERS, SOURCES] of var float: x;


constraint forall(c in CUSTOMERS, s in SOURCES)(x[c,s] >= 0);

constraint forall(s in SOURCES)(sum(c in CUSTOMERS)(x[c,s]) <= Supply[s]);

constraint forall(c in CUSTOMERS)(sum(s in SOURCES)(x[c,s]) = Demand[c]);



solve minimize sum(c in CUSTOMERS, s in SOURCES)(Tcost[c,s] * x[c,s]);




