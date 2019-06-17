set of int: I = 1..ncomp;

set of int: J = 1..neq;

array[I] of float: a;

int: neq;

array[I] of float: b;

array[I] of float: c;

array[I] of float: d;

float: f = f1 * f2 * f3 / f4;

float: f1;

float: f2;

float: f3;

float: f4;

int: ncomp;


array[I] of var float: x;


constraint forall(i in I)(assert(a[i] > 0, "Assertion a[\(i)] > 0 failed!"));

constraint assert(neq > 0, "Assertion neq > 0 failed!");

constraint forall(i in I)(assert(b[i] > 0, "Assertion b[\(i)] > 0 failed!"));

constraint forall(i in I)(assert(c[i] > 0, "Assertion c[\(i)] > 0 failed!"));

constraint forall(i in I)(assert(d[i] > 0, "Assertion d[\(i)] > 0 failed!"));

constraint assert(f1 > 0, "Assertion f1 > 0 failed!");

constraint assert(f2 > 0, "Assertion f2 > 0 failed!");

constraint assert(f3 > 0, "Assertion f3 > 0 failed!");

constraint assert(f4 > 0, "Assertion f4 > 0 failed!");

constraint assert(ncomp > 0, "Assertion ncomp > 0 failed!");

constraint forall(i in I)(x[i] >= 0);

constraint forall(i in J)(x[i + neq] / (b[i + neq] * sum(j in J)(x[j + neq] / b[j + neq])) = c[i] * x[i] / (40 * b[i] * sum(j in J)(x[j] / b[j])));

constraint sum(i in I)(x[i]) = 1;

constraint sum(i in J)(x[i] / d[i] + f * sum(i in J)(x[i + neq] / b[i + neq])) = 1.671;



solve minimize sum(i in I)(a[i] * x[i]);




