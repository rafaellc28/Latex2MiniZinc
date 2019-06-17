enum SCENARIOS;

enum PLANTS;

enum DEMAND;

array[PLANTS] of float: C;

array[PLANTS] of float: e;

array[DEMAND] of float: T;

array[PLANTS] of float: O;

array[DEMAND, SCENARIOS] of float: D;


var float: capcost;

array[SCENARIOS] of var float: v;

array[PLANTS] of var float: x;

array[PLANTS, DEMAND, SCENARIOS] of var float: y;


constraint forall(p in PLANTS)(x[p] >= 0);

constraint forall(p in PLANTS, d in DEMAND, s in SCENARIOS)(y[p,d,s] >= 0);

constraint capcost = sum(p in PLANTS)(C[p] * (e[p] + x[p]));

constraint forall(s in SCENARIOS)(v[s] = sum(p in PLANTS, d in DEMAND)(T[d] * O[p] * y[p,d,s]));

constraint forall(p in PLANTS, s in SCENARIOS)(e[p] + x[p] >= sum(d in DEMAND)(y[p,d,s]));

constraint forall(d in DEMAND, s in SCENARIOS)(D[d,s] = sum(p in PLANTS)(y[p,d,s]));



solve minimize capcost + sum(s in SCENARIOS)(0.25 * v[s]);




