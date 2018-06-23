enum T;

enum S;

array[int] of float: R;

float: Rportfolio;

array[int, int] of float: Rt;


array[INDEX_SET_y_1] of var float: y;

array[INDEX_SET_z_1] of var float: z;

array[INDEX_SET_w_1] of var float: w;

set of int: INDEX_SET_w_1 = S;

set of int: INDEX_SET_y_1 = T;

set of int: INDEX_SET_z_1 = T;


constraint forall(t in INDEX_SET_y_1)(y[t] >= 0);

constraint forall(t in INDEX_SET_z_1)(z[t] >= 0);

constraint forall(s in INDEX_SET_w_1)(w[s] >= 0);

constraint sum(s in S)(w[s] * R[s]) >= Rportfolio;

constraint sum(s in S)(w[s]) = 1;

constraint forall(t in T)((y[t] - z[t]) = sum(s in S)((Rt[s,t] - R[s]) * w[s]));



solve minimize (1 / card(T)) * sum(t in T)((y[t] + z[t]));




