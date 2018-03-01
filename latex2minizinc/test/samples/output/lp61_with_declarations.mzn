set of int: N = 1..n;

set of int: D = [i| i in U where sum(j in N)(a[j] * x[i,j]) <= b];

set of int: U = 0..floor(pow(2,n) - 1);

array[INDEX_SET_x_1, INDEX_SET_x_2] of float: x = array2d(INDEX_SET_x_1, INDEX_SET_x_2, [floor((i div floor(pow(2,j - 1)))) mod 2 | i in U, j in N]);

int: n;

array[int] of float: a;

float: b;


array[INDEX_SET_alfa_1] of var int: alfa;

var int: beta;

set of int: INDEX_SET_U_diff_D;

set of int: INDEX_SET_alfa_1;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;

array[INDEX_SET_U_diff_D] of int: U_diff_D;


constraint forall(j in N)(alfa[j] >= 0);

constraint beta >= 0;

constraint forall(i in D)(sum(j in N)(alfa[j] * x[i,j]) <= beta);

constraint forall(i in U_diff_D)(sum(j in N)(alfa[j] * x[i,j]) >= beta + 1);



solve minimize sum(j in N)(alfa[j] + beta);




