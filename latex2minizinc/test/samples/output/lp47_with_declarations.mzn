enum I;

array[int] of float: a;

float: BigM = 1 + sum(i in I)(abs(a[i]));

array[INDEX_SET_r_1] of float: r = array1d(INDEX_SET_r_1, [1 + sum(j in I)(if (a[j] < a[i] \/ a[j] = a[i] /\ j < i) then 1 else 0 endif) | i in I]);

array[INDEX_SET_s_1] of float: s = array1d(INDEX_SET_s_1, [1 + sum(j in I where a[i] < a[j] \/ a[i] = a[j] /\ i < j)(1) | i in I]);


array[INDEX_SET_y_1, INDEX_SET_y_2] of var bool: y;

array[INDEX_SET_t_1] of var float: t;

set of int: INDEX_SET_r_1;

set of int: INDEX_SET_s_1;

set of int: INDEX_SET_t_1 = I;

set of int: INDEX_SET_y_1 = I;

set of int: INDEX_SET_y_2 = I;


constraint forall(i in I, j in I where i != j)(a[i] <= a[j] + BigM * y[i,j]);

constraint forall(i in I, j in I where i != j)(a[j] <= a[i] + BigM * (1 - y[i,j]));

constraint forall(i in I, j in I where i != j)(y[i,j] + y[j,i] = 1);

constraint forall(i in I)(t[i] = 1 + sum(j in I where i != j)(y[i,j]));

solve satisfy;


