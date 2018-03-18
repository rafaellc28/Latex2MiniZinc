int: n = 7;

array[int] of int: base = [if i = 1 then 0 else sum(j in 1..floor(i - 1))(x[j]) endif | i in 1..n];

int: len = sum(i in 1..n)(x[i]);

array[int] of int: x = [3,2,0,5,4,3,4];


array[INDEX_SET_y_1] of var int: y;

set of int: INDEX_SET_y_1 = 1..len;


constraint y = [max(j in 1..n)(j * (i > base[j])) | i in 1..len];

solve satisfy;


