enum I;

array[int] of float: x;

array[int] of float: y;


array[INDEX_SET_u_1] of var float: u;

array[INDEX_SET_v_1] of var float: v;

var float: a;

var float: b;

set of int: INDEX_SET_u_1 = I;

set of int: INDEX_SET_v_1 = I;


constraint forall(i in INDEX_SET_u_1)(u[i] >= 0);

constraint forall(i in INDEX_SET_v_1)(v[i] >= 0);

constraint forall(i in I)(b * x[i] + a + u[i] - v[i] = y[i]);



solve minimize sum(i in I)(u[i] + sum(i in I)(v[i]));




