array[INDEX_SET_P] of set of int: P;

enum J;

array[int] of float: t;

set of int: INDEX_SET_P;


array[int] of var float: x;

var float: z;


constraint forall(j in J)(x[j] >= 0);

constraint forall(j in J, k in P[j])(x[j] >= x[to_enum(J,k)] + t[to_enum(J,k)]);

constraint forall(j in J)(z >= x[j] + t[j]);



var float: obj = z;

solve minimize obj;




