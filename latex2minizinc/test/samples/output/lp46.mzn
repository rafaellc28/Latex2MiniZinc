int: N;

array[0..N] of float: Xi;

array[0..N] of float: Fi;


var float: f;

array[1..N] of var float: s;

array[1..N] of var bool: z;

var float: x;


constraint forall(n in 1..N)(s[n] >= 0);

constraint forall(n in 1..N)(s[n] <= z[n]);

constraint 1 = sum(n in 1..N)(z[n]);

constraint x = sum(n in 1..N)((Xi[n - 1] * z[n] + (Xi[n] - Xi[n - 1]) * s[n]));

constraint f = sum(n in 1..N)((Fi[n - 1] * z[n] + (Fi[n] - Fi[n - 1]) * s[n]));

constraint forall(n in 0..N)(Xi[n] >= 0);

constraint forall(n in 0..N)(Fi[n] >= 0);



solve maximize f;




