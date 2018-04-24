int: n = 5;

array[int] of 1..n: b = [3,5,2,3,1];


array[INDEX_SET_a_1] of var 1..n: a;

set of int: INDEX_SET_a_1 = 1..n;


constraint forall(j in 1..n)(assert(n - j in 1..n,"b[\(n-j)]"));

constraint forall(j in 1..n, i in b[n - j]..n)(a[j] < i);

solve satisfy;


