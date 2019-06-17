int: n = 7;

array[1..n] of int: base = [if i = 1 then 0 else sum(j in 1..floor(i - 1))(x[j]) endif | i in 1..n];

int: len = sum(i in 1..n)(x[i]);

array[1..n] of int: x = [3,2,0,5,4,3,4];


array[1..len] of var int: y;


constraint y = [max(j in 1..n)(j * (i > base[j])) | i in 1..len];

solve satisfy;


