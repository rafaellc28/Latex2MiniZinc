set of int: T = 1..N;

enum S;

array[S] of float: r;

float: rportfolio;

array[S, T] of float: rt = array2d(S, T, [r[i] + sum(j in S where j <= i)(c[i,j] * zn[j,t]) | i in S, t in T]);

array[S, S] of float: cov;

array[S, S] of float: c;

float: utc = product(i in 1..2)((gmtime() - 1000000000));

float: seed = utc - 100000 * floor(utc / 100000);

int: N;

array[S, T] of float: zn = array2d(S, T, [Normal(0,1) | j in S, t in T]);


array[T] of var float: y;

array[T] of var float: z;

array[S] of var float: w;


constraint forall(i in S, j in S where i >= j)(c[i,j] = if i = j then sqrt(cov[i,i] - (sum(k in S where k < i)((c[i,k] * c[i,k])))) else (cov[i,j] - sum(k in S where k < j)(c[i,k] * c[j,k])) / c[j,j] endif);

constraint forall(t in T)(y[t] >= 0);

constraint forall(t in T)(z[t] >= 0);

constraint forall(s in S)(w[s] >= 0);

constraint sum(s in S)(w[s] * r[s]) >= rportfolio;

constraint sum(s in S)(w[s]) = 1;

constraint forall(t in T)((y[t] - z[t]) = sum(s in S)((rt[s,t] - r[s]) * w[s]));



solve minimize (1 / card(T)) * sum(t in T)((y[t] + z[t]));




