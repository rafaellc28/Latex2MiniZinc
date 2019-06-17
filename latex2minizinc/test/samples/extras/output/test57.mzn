enum I;

float: a;


array[I] of var int: A;

array[I] of var int: B;


constraint forall(i in I)(A[i] >= 0);

constraint forall(i in I)(B[i] >= 0);





solve minimize if a != 1 then sum(i in I)(A[i]) else sum(i in I)(A[i] + B[i]) endif;




