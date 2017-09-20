enum I;

enum J;

array[int, int] of float: C;


array[INDEX_SET_x_1, INDEX_SET_x_2] of var float: x;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;


constraint forall(i in I, j in J)(x[i,j] >= 0);

constraint forall(i in I)(sum(j in J)(x[i,j]) <= 1);

constraint forall(j in J)(sum(i in I)(x[i,j]) = 1);



var float: obj = sum(i in I, j in J)(C[i,j] * x[i,j]);

solve minimize obj;




