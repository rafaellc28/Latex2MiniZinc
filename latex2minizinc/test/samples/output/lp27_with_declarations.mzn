enum SCENARIOS;

enum PLANTS;

enum DEMAND;

array[int] of float: C;

array[int] of float: e;

array[int] of float: T;

array[int] of float: O;

array[int, int] of float: D;


var float: capcost;

array[int] of var float: v;

array[int] of var float: x;

array[int, int, int] of var float: y;


constraint forall(p in PLANTS)(x[p] >= 0);

constraint forall(p in PLANTS, d in DEMAND, s in SCENARIOS)(y[p,d,s] >= 0);

constraint capcost = sum(p in PLANTS)(C[p] * (e[p] + x[p]));

constraint forall(s in SCENARIOS)(v[s] = sum(p in PLANTS, d in DEMAND)(T[d] * O[p] * y[p,d,s]));

constraint forall(p in PLANTS, s in SCENARIOS)(e[p] + x[p] >= sum(d in DEMAND)(y[p,d,s]));

constraint forall(d in DEMAND, s in SCENARIOS)(D[d,s] = sum(p in PLANTS)(y[p,d,s]));



var float: obj = capcost + sum(s in SCENARIOS)(0.25 * v[s]);

solve minimize obj;




