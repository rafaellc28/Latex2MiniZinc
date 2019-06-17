int: N;

array[0..N] of float: xi;

array[0..N] of float: fi;


var float: f;

var float: x;

array[1..N] of var float: s;

array[1..N] of var bool: z;


constraint forall(n in 1..N)(s[n] >= 0);

constraint forall(n in 1..N)(s[n] <= z[n]);

constraint 1 = sum(n in 1..N)(z[n]);

constraint x = sum(n in 1..N)((xi[n - 1] * z[n] + (xi[n] - xi[n - 1]) * s[n]));

constraint f = sum(n in 1..N)((fi[n - 1] * z[n] + (fi[n] - fi[n - 1]) * s[n]));



solve maximize f;




