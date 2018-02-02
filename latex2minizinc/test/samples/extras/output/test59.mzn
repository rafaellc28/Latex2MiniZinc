enum I;

array[INDEX_SET_a_1] of float: a = array1d(INDEX_SET_a_1, [1 | i in I where t[i] = true]);

array[int] of float: t;

set of int: INDEX_SET_a_1;




solve satisfy;


