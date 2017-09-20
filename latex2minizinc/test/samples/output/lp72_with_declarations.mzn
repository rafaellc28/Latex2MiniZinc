set of int: I = 1..12;

array[int] of float: a;

array[int] of float: pos;

array[INDEX_SET_ind_1] of float: ind = array1d(INDEX_SET_ind_1, [sum(i in I where pos[i] = k)(i) | k in 1..card(I)]);

set of int: INDEX_SET_ind_1;




solve satisfy;


