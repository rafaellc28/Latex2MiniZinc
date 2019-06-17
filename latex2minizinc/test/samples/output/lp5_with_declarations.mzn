enum C;

set of int: N;

array[C, {price,weight} union N] of float: Data;

array[N] of float: Allowance;

int: price;

int: weight;


array[C] of var float: x;


constraint forall(c in C)(x[c] >= 0);

constraint forall(n in N)(sum(c in C)(Data[c,n] * x[c]) >= Allowance[n]);



solve minimize sum(c in C)(x[c]);




