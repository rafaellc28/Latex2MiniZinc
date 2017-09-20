enum T;

enum S;

array[int] of float: R;

float: Rportfolio;

array[int, int] of float: Rt;


array[INDEX_SET_y_1] of var float: y;

array[INDEX_SET_z_1] of var float: z;

array[INDEX_SET_w_1] of var float: w;

set of int: INDEX_SET_w_1;

set of int: INDEX_SET_y_1;

set of int: INDEX_SET_z_1;


constraint forall(t in T)(y[t] >= 0);

constraint forall(t in T)(z[t] >= 0);

constraint forall(s in S)(w[s] >= 0);

constraint sum(s in S)(w[s] * R[s]) >= Rportfolio;

constraint sum(s in S)(w[s]) = 1;

constraint forall(t in T)((y[t] - z[t]) = sum(s in S)((Rt[s,t] - R[s]) * w[s]));



var float: obj = (1 / card(T)) * sum(t in T)((y[t] + z[t]));

solve minimize obj;




