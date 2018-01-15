enum C;


array[INDEX_SET_x_1, INDEX_SET_x_2, INDEX_SET_x_3] of var int: x;

set of int: INDEX_SET_x_1 = 1..3;

set of int: INDEX_SET_x_2 = 2..4;

set of int: INDEX_SET_x_3 = 4..6;


constraint forall(i0 in INDEX_SET_x_1, i1 in INDEX_SET_x_2, i2 in INDEX_SET_x_3)(x[i0,i1,i2] >= 0);

constraint x[1,3,5] + x[1,4,6] <= 80;

constraint x[3,2,4] + x[3,2,5] <= 100;



var float: obj = sum(c in C)(3 * x[1,2,c] + 2 * x[2,2,c]);

solve maximize obj;




