enum I;

enum J;

array[INDEX_SET_c_1, INDEX_SET_c_2] of float: c = array2d(INDEX_SET_c_1, INDEX_SET_c_2, [f * d[i,j] / 1000 | i in I, j in J]);

array[int] of float: a;

array[int] of float: b;

array[int, int] of float: d;

float: f;


array[INDEX_SET_x_1, INDEX_SET_x_2] of var float: x;

set of int: INDEX_SET_c_1;

set of int: INDEX_SET_c_2;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;


constraint forall(i in I, j in J)(x[i,j] >= 0);

constraint forall(i in I)(sum(j in J)(x[i,j]) <= a[i]);

constraint forall(j in J)(sum(i in I)(x[i,j]) >= b[j]);



var float: obj = sum(i in I, j in J)(c[i,j] * x[i,j]);

solve minimize obj;




