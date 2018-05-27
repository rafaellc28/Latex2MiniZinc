enum I;

set of int: T = 1..N;

array[int] of float: Mu;

array[int, int] of float: Sigma;

int: N;

array[int, int] of float: Chol;

float: utc = product(i in 1..2)((gmtime() - 1000000000));

float: seed = utc - 100000 * floor(utc / 100000);

array[INDEX_SET_z_1, INDEX_SET_z_2] of float: z = array2d(INDEX_SET_z_1, INDEX_SET_z_2, [Normal(0,1) | i in I, t in T]);

array[INDEX_SET_x_1, INDEX_SET_x_2] of float: x = array2d(INDEX_SET_x_1, INDEX_SET_x_2, [Mu[i] + sum(j in I where i >= j)(Chol[i,j] * z[j,t]) | i in I, t in T]);

array[INDEX_SET_xbar_1] of float: xbar = array1d(INDEX_SET_xbar_1, [(1 / card(T)) * sum(t in T)(x[i,t]) | i in I]);

array[INDEX_SET_Cov_1, INDEX_SET_Cov_2] of float: Cov = array2d(INDEX_SET_Cov_1, INDEX_SET_Cov_2, [(1 / card(T)) * sum(t in T)((x[i,t] - xbar[i]) * (x[j,t] - xbar[j])) | i,j in I]);

set of int: INDEX_SET_Cov_1;

set of int: INDEX_SET_Cov_2;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;

set of int: INDEX_SET_xbar_1;

set of int: INDEX_SET_z_1;

set of int: INDEX_SET_z_2;


constraint forall(i,j in I where i >= j)(Chol[i,j] = if i = j then sqrt(Sigma[i,i] - (sum(k in I where k < i)((Chol[i,k] * Chol[i,k])))) else (Sigma[i,j] - sum(k in I where k < j)(Chol[i,k] * Chol[j,k])) / Chol[j,j] endif);



solve satisfy;


