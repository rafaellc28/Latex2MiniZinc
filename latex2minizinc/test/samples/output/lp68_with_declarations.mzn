int: n;

array[1..n] of float: a = array1d(1..n, [pow(2,k + n + 1) + pow(2,k + n + 1 - j) + 1 | j in 1..n]);

float: b = 0.5 * floor(sum(j in 1..n)(a[j]));

float: log2n = ln(n) / ln(2);

float: k = floor(log2n);


array[1..n] of var bool: x;


constraint assert(n > 0, "Assertion n > 0 failed!");

constraint sum(j in 1..n)(a[j] * x[j]) <= b;



solve maximize sum(j in 1..n)(a[j] * x[j]);




