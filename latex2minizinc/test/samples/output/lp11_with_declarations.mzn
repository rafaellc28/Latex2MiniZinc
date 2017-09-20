array[INDEX_SET_P] of set of int: P;

enum J;

array[int] of float: t;


array[INDEX_SET_x_1] of var float: x;

var float: z;

set of int: INDEX_SET_P;

set of int: INDEX_SET_x_1;


constraint forall(j in J)(x[j] >= 0);

constraint forall(j in J, k in P[j])(x[j] >= x[to_enum(J,k)] + t[to_enum(J,k)]);

constraint forall(j in J)(z >= x[j] + t[j]);



var float: obj = z;

solve minimize obj;




