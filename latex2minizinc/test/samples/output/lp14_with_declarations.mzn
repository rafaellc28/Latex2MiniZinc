enum CUSTOMERS;

enum SOURCES;

array[int, int] of float: Tcost;

array[int] of float: Supply;

array[int] of float: Demand;


array[int, int] of var float: x;


constraint forall(c in CUSTOMERS, s in SOURCES)(x[c,s] >= 0);

constraint forall(s in SOURCES)(sum(c in CUSTOMERS)(x[c,s]) <= Supply[s]);

constraint forall(c in CUSTOMERS)(sum(s in SOURCES)(x[c,s]) = Demand[c]);



var float: obj = sum(c in CUSTOMERS, s in SOURCES)(Tcost[c,s] * x[c,s]);

solve minimize obj;




