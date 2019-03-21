set of int: INDEX_SET_I_diff_J;

array[INDEX_SET_I_diff_J] of int: I_diff_J;


constraint let {array[int] of var int: x; array[int] of var int: y = [i | i in I_diff_J]} in
	x[1];

solve satisfy;


