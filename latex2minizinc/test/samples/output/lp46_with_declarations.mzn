int: N;

array[int] of float: xi;

array[int] of float: fi;


var float: f;

var float: x;

array[INDEX_SET_s_1] of var float: s;

array[INDEX_SET_z_1] of var bool: z;

set of int: INDEX_SET_s_1 = 1..N;

set of int: INDEX_SET_z_1 = 1..N;


constraint forall(n in INDEX_SET_s_1)(s[n] >= 0);

constraint forall(n in 1..N)(s[n] <= z[n]);

constraint 1 = sum(n in 1..N)(z[n]);

constraint x = sum(n in 1..N)((xi[n - 1] * z[n] + (xi[n] - xi[n - 1]) * s[n]));

constraint f = sum(n in 1..N)((fi[n - 1] * z[n] + (fi[n] - fi[n - 1]) * s[n]));



var float: obj = f;

solve maximize obj;




