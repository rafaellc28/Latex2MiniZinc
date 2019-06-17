enum I;

array[1..I] of float: c;

array[1..I] of float: d;

array[I] of float: a;

array[I] of float: b;


constraint forall(i in 1..I)(c[i] > d[i]);

constraint forall(i in I)(a[i] < b[i]);

solve satisfy;


