enum C;


array[INDEX_SET_x_1, INDEX_SET_x_2, INDEX_SET_x_3] of var int: x;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;

set of int: INDEX_SET_x_3;


constraint forall(i0 in 1..2, i1 in 1..2, i2 in 1..2)(x[i0,i1,i2] >= 0);

constraint 1.85 * x[1,1,1] + x[2,2,2] <= 100;

constraint x[1,2,1] + x[2,1,1] <= 80;

constraint x[1,1,1] <= 40;



var float: obj = sum(c in C)(3 * x[1,1,c] + 2 * x[2,2,c]);

solve maximize obj;




