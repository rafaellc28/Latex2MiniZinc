int: N;

array[int] of float: Xi;

array[int] of float: Fi;


var float: f;

array[INDEX_SET_s_1] of var float: s;

array[INDEX_SET_z_1] of var bool: z;

var float: x;

set of int: INDEX_SET_s_1;

set of int: INDEX_SET_z_1;


constraint forall(n in 1..N)(s[n] >= 0);

constraint forall(n in 1..N)(s[n] <= z[n]);

constraint 1 = sum(n in 1..N)(z[n]);

constraint x = sum(n in 1..N)((Xi[n - 1] * z[n] + (Xi[n] - Xi[n - 1]) * s[n]));

constraint f = sum(n in 1..N)((Fi[n - 1] * z[n] + (Fi[n] - Fi[n - 1]) * s[n]));

constraint forall(n in 0..N)(Xi[n] >= 0);

constraint forall(n in 0..N)(Fi[n] >= 0);



var float: obj = f;

solve maximize obj;




