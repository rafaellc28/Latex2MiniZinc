enum J;

array[INDEX_SET_P] of set of int: P;

array[int] of float: T;

set of int: INDEX_SET_P;


array[int] of var float: x;

var float: z;


constraint forall(j in J)(x[j] >= 0);

constraint forall(j in J, k in P[j])(x[j] >= x[to_enum(J,k)] + T[to_enum(J,k)]);

constraint forall(j in J)(z >= x[j] + T[j]);

constraint forall(j in J)(T[j] >= 0);



var float: obj = z;

solve minimize obj;




