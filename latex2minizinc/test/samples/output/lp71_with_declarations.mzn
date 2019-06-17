enum I;

set of int: T = 1..N;

array[I] of float: Mu;

array[I, I] of float: Sigma;

int: N;

array[I, I] of float: Chol;

float: utc = product(i in 1..2)((gmtime() - 1000000000));

float: seed = utc - 100000 * floor(utc / 100000);

array[I, T] of float: z = array2d(I, T, [Normal(0,1) | i in I, t in T]);

array[I, T] of float: x = array2d(I, T, [Mu[i] + sum(j in I where i >= j)(Chol[i,j] * z[j,t]) | i in I, t in T]);

array[I] of float: xbar = array1d(I, [(1 / card(T)) * sum(t in T)(x[i,t]) | i in I]);

array[I, I] of float: Cov = array2d(I, I, [(1 / card(T)) * sum(t in T)((x[i,t] - xbar[i]) * (x[j,t] - xbar[j])) | i,j in I]);


constraint assert(N >= 1, "Assertion N >= 1 failed!");

constraint forall(i,j in I where i >= j)(Chol[i,j] = if i = j then sqrt(Sigma[i,i] - (sum(k in I where k < i)((Chol[i,k] * Chol[i,k])))) else (Sigma[i,j] - sum(k in I where k < j)(Chol[i,k] * Chol[j,k])) / Chol[j,j] endif);



solve satisfy;


