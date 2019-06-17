set of int: I = 1..5;

set of int: J = 1..4;

array[I, J] of float: a;

array[I] of float: c;


array[J] of var float: x = array1d(J, [j | j in J]);


constraint forall(j in J)(x[j] >= 0 /\ x[j] <= 10);





solve minimize -sum(i in I)(1 / (sum(j in J)(pow((x[j] - a[i,j]),2) + c[i])));




