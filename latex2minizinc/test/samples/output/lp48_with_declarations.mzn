set of int: J = 1..n;

set of int: I = 1..m;

array[int] of float: w;

float: c;

int: m;

array[int, int] of bool: z;

int: n = sum(j in 1..m)(if exists(i in I)(z[i,j] = true) then 1 else 0 endif);


array[INDEX_SET_used_1] of var bool: used;

array[INDEX_SET_x_1, INDEX_SET_x_2] of var bool: x;

set of int: INDEX_SET_used_1;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;


constraint forall(i in I, j in 1..m)(z[i,j] = if i = 1 /\ j = 1 then 1 else if exists(jj in 1..floor(j - 1))(z[i,jj] = true) then 0 else if sum(ii in 1..floor(i - 1))(w[ii] * z[ii,j] + w[i]) > c then 0 else 1 endif endif endif);

constraint forall(i in I)(sum(j in J)(x[i,j]) = 1);

constraint forall(j in J)(sum(i in I)(w[i] * x[i,j]) <= c * used[j]);



var float: obj = sum(j in J)(used[j]);

solve minimize obj;




