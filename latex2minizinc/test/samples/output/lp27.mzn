enum SCENARIOS;

enum PLANTS;

enum DEMAND;

array[int] of float: C;

array[int] of float: E;

array[int] of float: T;

array[int] of float: O;

array[int, int] of float: D;


var float: capcost;

array[INDEX_SET_v_1] of var float: v;

array[INDEX_SET_x_1] of var float: x;

array[INDEX_SET_y_1, INDEX_SET_y_2, INDEX_SET_y_3] of var float: y;

set of int: INDEX_SET_v_1 = SCENARIOS;

set of int: INDEX_SET_x_1 = PLANTS;

set of int: INDEX_SET_y_1 = PLANTS;

set of int: INDEX_SET_y_2 = DEMAND;

set of int: INDEX_SET_y_3 = SCENARIOS;


constraint forall(p in INDEX_SET_x_1)(x[p] >= 0);

constraint forall(p in INDEX_SET_y_1, d in INDEX_SET_y_2, s in INDEX_SET_y_3)(y[p,d,s] >= 0);

constraint capcost = sum(p in PLANTS)(C[p] * (E[p] + x[p]));

constraint forall(s in SCENARIOS)(v[s] = sum(p in PLANTS, d in DEMAND)(T[d] * O[p] * y[p,d,s]));

constraint forall(p in PLANTS, s in SCENARIOS)(E[p] + x[p] >= sum(d in DEMAND)(y[p,d,s]));

constraint forall(d in DEMAND, s in SCENARIOS)(D[d,s] = sum(p in PLANTS)(y[p,d,s]));



solve minimize capcost + sum(s in SCENARIOS)(0.25 * v[s]);




