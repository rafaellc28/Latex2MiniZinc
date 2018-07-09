enum P;

enum R;

int: T;

array[int, int] of float: c;

array[int] of float: d;

array[int] of float: f;

float: M;

array[int] of float: b;

array[int, int] of float: a;


array[INDEX_SET_x_1, INDEX_SET_x_2] of var float: x;

array[INDEX_SET_s_1, INDEX_SET_s_2] of var float: s;

set of int: INDEX_SET_s_1 = R;

set of int: INDEX_SET_s_2 = 1..floor(T + 1);

set of int: INDEX_SET_x_1 = P;

set of int: INDEX_SET_x_2 = 1..T;


constraint assert(T > 0, "Assertion T > 0 failed!");

constraint assert(M > 0, "Assertion M > 0 failed!");

constraint forall(r in R)(assert(b[r] >= 0, "Assertion b[\(r)] >= 0 failed!"));

constraint forall(r in R)(assert(a[r,r] >= 0, "Assertion a[\(r),\(r)] >= 0 failed!"));

constraint forall(p in INDEX_SET_x_1, t in INDEX_SET_x_2)(x[p,t] >= 0);

constraint forall(r in INDEX_SET_s_1, t1 in INDEX_SET_s_2)(s[r,t1] >= 0);

constraint forall(t in 1..T)(sum(j in P)(x[j,t]) <= M);

constraint forall(i in R)(s[i,1] <= b[i]);

constraint forall(i in R, t in 1..T)(s[i,t + 1] = s[i,t] - sum(j in P)(a[i,j] * x[j,t]));



solve maximize sum(t in 1..T)((sum(j in P)(c[j,t] * x[j,t] - sum(i in R)(d[i] * s[i,t]))) + sum(i in R)(f[i] * s[i,T + 1]));




