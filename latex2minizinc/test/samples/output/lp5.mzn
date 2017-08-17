enum C;

enum N;

array[C, N] of float: Data;

array[N] of float: Allowance;


array[C] of var float: x;


constraint forall(c in C)(x[c] >= 0);

constraint forall(n in N)(sum(c in C)(Data[c,n] * x[c]) >= Allowance[n]);



var float: obj = sum(c in C)(x[c]);

solve minimize obj;




