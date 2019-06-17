enum J;

enum M;

array[J, 1..MS] of M: Sigma;

array[J, M] of float: P;

int: MS;

float: K;


array[J, M] of var float: x;

array[J, J, M] of var bool: Y;

var float: z;


constraint forall(j in J, a in M)(x[j,a] >= 0);

constraint forall(j in J, t in 2..MS)(x[j,Sigma[j,t]] >= x[j,Sigma[j,t - 1]] + P[j,Sigma[j,t - 1]]);

constraint forall(i in J, j in J, a in M where i != j)(x[i,a] >= x[j,a] + P[j,a] - K * Y[i,j,a]);

constraint forall(i in J, j in J, a in M where i != j)(x[j,a] >= x[i,a] + P[i,a] - K * (1 - Y[i,j,a]));

constraint forall(j in J)(z >= x[j,Sigma[j,MS]] + P[j,Sigma[j,MS]]);

constraint forall(j in J, t in 1..MS)(Sigma[j,t] >= 1 /\ Sigma[j,t] <= MS);

constraint forall(j in J, a in M)(P[j,a] >= 0);

constraint forall(j in J, a in M)(x[j,a] >= 0);



solve minimize z;




