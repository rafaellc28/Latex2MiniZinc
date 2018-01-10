enum C;


array[INDEX_SET_x_1, INDEX_SET_x_2, INDEX_SET_x_3] of var int: x;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;

set of int: INDEX_SET_x_3;


constraint forall(i0 in 1..3, c in C, i1 in 2..6)(x[i0,c,i1] >= 0);

constraint x[1,3,5] + x[1,4,6] <= 80;

constraint x[3,2,4] + x[3,2,5] <= 100;



var float: obj = sum(c in C)(3 * x[1,c,2] + 2 * x[2,c,2]);

solve maximize obj;




