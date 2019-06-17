enum I;

array[I] of float: x;

array[I] of float: y;


var float: z;

var float: a;

var float: b;

array[I] of var float: u;

array[I] of var float: v;


constraint forall(i in I)(u[i] >= 0);

constraint forall(i in I)(v[i] >= 0);

constraint forall(i in I)(b * x[i] + a + u[i] - v[i] = y[i]);

constraint forall(i in I)(z - u[i] >= 0);

constraint forall(i in I)(z - v[i] >= 0);



solve minimize z;




