int: n;

array[INDEX_SET_a_1] of float: a = array1d(INDEX_SET_a_1, [pow(2,k + n + 1) + pow(2,k + n + 1 - j) + 1 | j in 1..n]);

float: b = 0.5 * floor(sum(j in 1..n)(a[j]));

float: log2n = ln(n) / ln(2);

float: k = floor(log2n);


array[INDEX_SET_x_1] of var bool: x;

set of int: INDEX_SET_a_1 = 1..n;

set of int: INDEX_SET_x_1 = 1..n;


constraint assert(n > 0, "Assertion n > 0 failed!");

constraint sum(j in 1..n)(a[j] * x[j]) <= b;



solve maximize sum(j in 1..n)(a[j] * x[j]);




