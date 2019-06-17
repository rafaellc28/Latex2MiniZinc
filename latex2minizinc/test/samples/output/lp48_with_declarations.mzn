set of int: J = 1..n;

set of int: I = 1..m;

array[1..m] of float: w;

float: c;

int: m;

array[I, 1..m] of bool: z;

int: n = sum(j in 1..m)(if exists(i in I)(z[i,j] = true) then 1 else 0 endif);


array[J] of var bool: used;

array[I, J] of var bool: x;


constraint forall(i in 1..m)(assert(w[i] > 0, "Assertion w[\(i)] > 0 failed!"));

constraint assert(c > 0, "Assertion c > 0 failed!");

constraint assert(m > 0, "Assertion m > 0 failed!");

constraint forall(i in I, j in 1..m)(z[i,j] = if i = 1 /\ j = 1 then 1 else if exists(jj in 1..floor(j - 1))(z[i,jj] = true) then 0 else if sum(ii in 1..floor(i - 1))(w[ii] * z[ii,j] + w[i]) > c then 0 else 1 endif endif endif);

constraint forall(i in I)(sum(j in J)(x[i,j]) = 1);

constraint forall(j in J)(sum(i in I)(w[i] * x[i,j]) <= c * used[j]);



solve minimize sum(j in J)(used[j]);




