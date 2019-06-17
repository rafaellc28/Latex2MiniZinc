enum T;

enum S;

array[S] of float: R;

float: Rportfolio;

array[S, T] of float: Rt;


array[T] of var float: y;

array[T] of var float: z;

array[S] of var float: w;


constraint forall(t in T)(y[t] >= 0);

constraint forall(t in T)(z[t] >= 0);

constraint forall(s in S)(w[s] >= 0);

constraint sum(s in S)(w[s] * R[s]) >= Rportfolio;

constraint sum(s in S)(w[s]) = 1;

constraint forall(t in T)((y[t] - z[t]) = sum(s in S)((Rt[s,t] - R[s]) * w[s]));



solve minimize (1 / card(T)) * sum(t in T)((y[t] + z[t]));




