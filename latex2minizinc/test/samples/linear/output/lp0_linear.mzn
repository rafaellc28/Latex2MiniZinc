enum INPUT;

enum OUTPUT;

array[INPUT] of float: cost;

array[OUTPUT] of float: out_min;

array[OUTPUT, INPUT] of float: io;

array[OUTPUT] of float: out_max;

array[INPUT] of float: in_min;

array[INPUT] of float: in_max;


array[INPUT] of var float: X;


constraint forall(i in INPUT)(assert(cost[i] > 0, "Assertion cost[\(i)] > 0 failed!"));

constraint forall(o in OUTPUT)(assert(out_min[o] >= 0, "Assertion out_min[\(o)] >= 0 failed!"));

constraint forall(o in OUTPUT, i in INPUT)(assert(io[o,i] >= 0, "Assertion io[\(o),\(i)] >= 0 failed!"));

constraint forall(o in OUTPUT)(assert(out_max[o] >= out_min[o], "Assertion out_max[\(o)] >= out_min[\(o)] failed!"));

constraint forall(i in INPUT)(assert(in_min[i] >= 0, "Assertion in_min[\(i)] >= 0 failed!"));

constraint forall(i in INPUT)(assert(in_max[i] >= in_min[i], "Assertion in_max[\(i)] >= in_min[\(i)] failed!"));

constraint forall(j in INPUT)(X[j] <= in_max[j] /\ X[j] >= in_min[j]);

constraint forall(i in OUTPUT)(sum(j in INPUT)(io[i,j] * X[j]) <= out_max[i] /\ sum(j in INPUT)(io[i,j] * X[j]) >= out_min[i]);



solve minimize sum(j in INPUT)(cost[j] * X[j]);




