set of int: J = 1..n;

set of int: M = 1..m;

array[int, int] of int: sigma;

array[int, int] of float: p;

int: m;

float: K = sum(j in J, a in M)(p[j,a]);

int: n;


array[INDEX_SET_x_1, INDEX_SET_x_2] of var float: x;

array[INDEX_SET_Y_1, INDEX_SET_Y_2, INDEX_SET_Y_3] of var bool: Y;

var float: z;

set of int: INDEX_SET_Y_1 = J;

set of int: INDEX_SET_Y_2 = J;

set of int: INDEX_SET_Y_3 = M;

set of int: INDEX_SET_x_1 = J;

set of int: INDEX_SET_x_2 = M;


constraint forall(j in J, a in M)(assert(p[j,a] >= 0, "Assertion p[\(j),\(a)] >= 0 failed!"));

constraint forall(j in INDEX_SET_x_1, a in INDEX_SET_x_2)(x[j,a] >= 0);

constraint forall(j in J, t in 2..m)(x[j,sigma[j,t]] >= x[j,sigma[j,t - 1]] + p[j,sigma[j,t - 1]]);

constraint forall(i in J, j in J, a in M where i != j)(x[i,a] >= x[j,a] + p[j,a] - K * Y[i,j,a]);

constraint forall(i in J, j in J, a in M where i != j)(x[j,a] >= x[i,a] + p[i,a] - K * (1 - Y[i,j,a]));

constraint forall(j in J)(z >= x[j,sigma[j,m]] + p[j,sigma[j,m]]);



solve minimize z;




