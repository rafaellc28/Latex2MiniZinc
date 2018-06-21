enum I;

array[int] of float: c;

array[int] of float: d;

array[int] of float: a;

array[int] of float: b;


constraint forall(i in 1..I)(c[i] > d[i]);

constraint forall(i in I)(a[i] < b[i]);

solve satisfy;


