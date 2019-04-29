array[INDEX_SET_x_1, INDEX_SET_x_2] of var 0..2: x;

set of int: INDEX_SET_x_1 = 0..2;

set of int: INDEX_SET_x_2 = 0..2;


constraint sum(i in 0..2)(x[i,i]) <= 1;

constraint x[x[1,1],1] = 2;

solve satisfy;


