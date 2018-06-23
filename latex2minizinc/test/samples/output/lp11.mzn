enum J;

array[INDEX_SET_P] of set of int: P;

array[int] of float: T;


array[INDEX_SET_x_1] of var float: x;

var float: z;

set of int: INDEX_SET_P;

set of int: INDEX_SET_x_1 = J;


constraint forall(j in INDEX_SET_x_1)(x[j] >= 0);

constraint forall(j in J, k in P[j])(x[j] >= x[k] + T[k]);

constraint forall(j in J)(z >= x[j] + T[j]);

constraint forall(j in J)(T[j] >= 0);



solve minimize z;




