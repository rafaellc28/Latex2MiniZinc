set of int: I = 1..ncomp;

set of int: J = 1..neq;

array[int] of float: a;

int: neq;

array[int] of float: b;

array[int] of float: c;

array[int] of float: d;

float: f = f1 * f2 * f3 / f4;

float: f1;

float: f2;

float: f3;

float: f4;

int: ncomp;


array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_x_1 = I;


constraint assert(neq > 0, "Assertion neq > 0 failed!");

constraint assert(ncomp > 0, "Assertion ncomp > 0 failed!");

constraint forall(i in INDEX_SET_x_1)(x[i] >= 0);

constraint forall(i in J)(x[i + neq] / (b[i + neq] * sum(j in J)(x[j + neq] / b[j + neq])) = c[i] * x[i] / (40 * b[i] * sum(j in J)(x[j] / b[j])));

constraint sum(i in I)(x[i]) = 1;

constraint sum(i in J)(x[i] / d[i] + f * sum(i in J)(x[i + neq] / b[i + neq])) = 1.671;



solve minimize sum(i in I)(a[i] * x[i]);




