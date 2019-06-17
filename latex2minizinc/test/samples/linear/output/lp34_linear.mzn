enum P;

enum R;

int: T;

array[P, 1..T] of float: c;

array[R] of float: d;

array[R] of float: f;

float: M;

array[R] of float: b;

array[R, P] of float: a;


array[P, 1..T] of var float: x;

array[R, 1..floor(T + 1)] of var float: s;


constraint assert(T > 0, "Assertion T > 0 failed!");

constraint assert(M > 0, "Assertion M > 0 failed!");

constraint forall(r in R)(assert(b[r] >= 0, "Assertion b[\(r)] >= 0 failed!"));

constraint forall(r in R, p in P)(assert(a[r,p] >= 0, "Assertion a[\(r),\(p)] >= 0 failed!"));

constraint forall(p in P, t in 1..T)(x[p,t] >= 0);

constraint forall(r in R, t1 in 1..floor(T + 1))(s[r,t1] >= 0);

constraint forall(t in 1..T)(sum(j in P)(x[j,t]) <= M);

constraint forall(i in R)(s[i,1] <= b[i]);

constraint forall(i in R, t in 1..T)(s[i,t + 1] = s[i,t] - sum(j in P)(a[i,j] * x[j,t]));



solve maximize sum(t in 1..T)((sum(j in P)(c[j,t] * x[j,t] - sum(i in R)(d[i] * s[i,t]))) + sum(i in R)(f[i] * s[i,T + 1]));




