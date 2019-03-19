constraint let {array[int] of var int: x; array[int] of var int: y; constraint y[i] = [i | i in I_diff_J]} in
	x[1];

solve satisfy;


