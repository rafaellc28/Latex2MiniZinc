set of int: J = 1..n;

set of int: M = 1..m;

array[J, 1..m] of int: sigma;

array[J, M] of float: p;

int: m;

float: K = sum(j in J, a in M)(p[j,a]);

int: n;


array[J, M] of var float: x;

array[J, J, M] of var bool: Y;

var float: z;


constraint forall(j in J, a in M)(assert(p[j,a] >= 0, "Assertion p[\(j),\(a)] >= 0 failed!"));

constraint assert(m > 0, "Assertion m > 0 failed!");

constraint assert(n > 0, "Assertion n > 0 failed!");

constraint forall(j in J, a in M)(x[j,a] >= 0);

constraint forall(j in J, t in 2..m)(x[j,sigma[j,t]] >= x[j,sigma[j,t - 1]] + p[j,sigma[j,t - 1]]);

constraint forall(i in J, j in J, a in M where i != j)(x[i,a] >= x[j,a] + p[j,a] - K * Y[i,j,a]);

constraint forall(i in J, j in J, a in M where i != j)(x[j,a] >= x[i,a] + p[i,a] - K * (1 - Y[i,j,a]));

constraint forall(j in J)(z >= x[j,sigma[j,m]] + p[j,sigma[j,m]]);



solve minimize z;




