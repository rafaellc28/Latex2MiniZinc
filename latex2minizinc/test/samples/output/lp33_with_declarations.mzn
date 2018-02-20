set of int: T = 1..N;

enum S;

array[int] of float: r;

float: rportfolio;

array[INDEX_SET_rt_1, INDEX_SET_rt_2] of float: rt = array2d(INDEX_SET_rt_1, INDEX_SET_rt_2, [r[i] + sum(j in S where j <= i)(c[i,j] * zn[j,t]) | i in S, t in T]);

array[int, int] of float: cov;

array[int, int] of float: c;

float: utc;

float: seed = utc - 100000 * floor(utc / 100000);

int: N;

array[int, int] of float: zn;


array[INDEX_SET_y_1] of var float: y;

array[INDEX_SET_z_1] of var float: z;

array[INDEX_SET_w_1] of var float: w;

set of int: INDEX_SET_rt_1;

set of int: INDEX_SET_rt_2;

set of int: INDEX_SET_w_1;

set of int: INDEX_SET_y_1;

set of int: INDEX_SET_z_1;


constraint forall(i in S, j in S where i >= j)(c[i,j] = if i = j then sqrt(cov[i,i] - (sum(k in S where k < i)((c[i,k] * c[i,k])))) else (cov[i,j] - sum(k in S where k < j)(c[i,k] * c[j,k])) / c[j,j] endif);

constraint forall(t in T)(y[t] >= 0);

constraint forall(t in T)(z[t] >= 0);

constraint forall(s in S)(w[s] >= 0);

constraint sum(s in S)(w[s] * r[s]) >= rportfolio;

constraint sum(s in S)(w[s]) = 1;

constraint forall(t in T)((y[t] - z[t]) = sum(s in S)((rt[s,t] - r[s]) * w[s]));



solve minimize (1 / card(T)) * sum(t in T)((y[t] + z[t]));




