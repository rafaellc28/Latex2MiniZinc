array[int] of float: A;

int: N;

float: B;


array[INDEX_SET_x_1] of var bool: x;

set of int: INDEX_SET_x_1 = 1..N;


constraint sum(j in 1..N)(A[j] * x[j]) <= B;



var float: obj = sum(j in 1..N)(A[j] * x[j]);

solve maximize obj;




