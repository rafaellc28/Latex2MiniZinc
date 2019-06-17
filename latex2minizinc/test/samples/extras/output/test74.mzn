enum I;

array[I] of float: a;

array[I] of float: b;

array[1..I] of float: c;

array[1..I] of float: d;


constraint forall(i in I)(a[i] < b[i]);

constraint forall(i in 1..I)(c[i] > d[i]);

solve satisfy;


