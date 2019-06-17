enum I;

array[I] of float: x;

array[I] of float: y;


array[I] of var float: u;

array[I] of var float: v;

var float: a;

var float: b;


constraint forall(i in I)(u[i] >= 0);

constraint forall(i in I)(v[i] >= 0);

constraint forall(i in I)(b * x[i] + a + u[i] - v[i] = y[i]);



solve minimize sum(i in I)(u[i] + sum(i in I)(v[i]));




