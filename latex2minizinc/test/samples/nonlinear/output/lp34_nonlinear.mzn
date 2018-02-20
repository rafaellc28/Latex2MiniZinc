set of int: I = 1..5;

set of int: J = 1..4;

array[int, int] of float: a;

array[int] of float: c;


array[INDEX_SET_x_1] of var float: x = array1d(J, [j | j in J]);

set of int: INDEX_SET_x_1;


constraint forall(j in J)(x[j] >= 0 /\ x[j] <= 10);





solve minimize -sum(i in I)(1 / (sum(j in J)(pow((x[j] - a[i,j]),2) + c[i])));




