set of int: I = 1..12;

array[INDEX_SET_a_1] of float: a = array1d(INDEX_SET_a_1, [Uniform(2,7) | i in I]);

array[int] of float: pos;

array[INDEX_SET_ind_1] of float: ind = array1d(INDEX_SET_ind_1, [sum(i in I where pos[i] = k)(i) | k in 1..card(I)]);

set of int: INDEX_SET_a_1;

set of int: INDEX_SET_ind_1 = 1..card(I);




solve satisfy;


