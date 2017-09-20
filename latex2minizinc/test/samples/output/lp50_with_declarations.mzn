enum I;

array[int] of float: x;

array[int] of float: y;


var float: z;

var float: a;

var float: b;

array[INDEX_SET_u_1] of var float: u;

array[INDEX_SET_v_1] of var float: v;

set of int: INDEX_SET_u_1;

set of int: INDEX_SET_v_1;


constraint forall(i in I)(u[i] >= 0);

constraint forall(i in I)(v[i] >= 0);

constraint forall(i in I)(b * x[i] + a + u[i] - v[i] = y[i]);

constraint forall(i in I)(z - u[i] >= 0);

constraint forall(i in I)(z - v[i] >= 0);



var float: obj = z;

solve minimize obj;




