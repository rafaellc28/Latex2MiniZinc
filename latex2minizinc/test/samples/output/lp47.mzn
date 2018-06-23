enum I;

array[int] of float: A;

float: BigM;


array[INDEX_SET_y_1, INDEX_SET_y_2] of var bool: y;

array[INDEX_SET_t_1] of var float: t;

set of int: INDEX_SET_t_1 = I;

set of int: INDEX_SET_y_1 = I;

set of int: INDEX_SET_y_2 = I;


constraint forall(i in I, j in I where i != j)(A[i] <= A[j] + BigM * y[i,j]);

constraint forall(i in I, j in I where i != j)(A[j] <= A[i] + BigM * (1 - y[i,j]));

constraint forall(i in I, j in I where i != j)(y[i,j] + y[j,i] = 1);

constraint forall(i in I)(t[i] = 1 + sum(j in I where i != j)(y[i,j]));

solve satisfy;


