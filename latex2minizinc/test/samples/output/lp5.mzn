enum C;

enum N;

array[int, int] of float: Data;

array[int] of float: Allowance;


array[int] of var float: x;


constraint forall(c in C)(x[c] >= 0);

constraint forall(n in N)(sum(c in C)(Data[c,n] * x[c]) >= Allowance[n]);



var float: obj = sum(c in C)(x[c]);

solve minimize obj;




