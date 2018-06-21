enum I;

array[int] of float: a;

array[int] of float: b;

array[int] of float: c;

array[int] of float: d;


constraint forall(i in I)(a[i] < b[i]);

constraint forall(i in 1..I)(c[i] > d[i]);

solve satisfy;


