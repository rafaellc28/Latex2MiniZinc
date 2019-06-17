enum I;

enum J;

array[I, J] of float: c = array2d(I, J, [f * d[i,j] / 1000 | i in I, j in J]);

array[I] of float: a;

array[J] of float: b;

array[I, J] of float: d;

float: f;


array[I, J] of var float: x;


constraint forall(i in I, j in J)(x[i,j] >= 0);

constraint forall(i in I)(sum(j in J)(x[i,j]) <= a[i]);

constraint forall(j in J)(sum(i in I)(x[i,j]) >= b[j]);



solve minimize sum(i in I, j in J)(c[i,j] * x[i,j]);




