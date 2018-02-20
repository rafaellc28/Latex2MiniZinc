enum I;

float: a;


array[INDEX_SET_A_1] of var int: A;

array[INDEX_SET_B_1] of var int: B;

set of int: INDEX_SET_A_1;

set of int: INDEX_SET_B_1;


constraint forall(i in I)(A[i] >= 0);

constraint forall(i in I)(B[i] >= 0);





solve minimize if a != 1 then sum(i in I)(A[i]) else sum(i in I)(A[i] + B[i]) endif;




