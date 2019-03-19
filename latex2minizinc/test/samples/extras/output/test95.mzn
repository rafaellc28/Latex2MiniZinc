constraint let {array[int] of var int: x; array[int] of int: y = [i | i in I where not(i in J)]} in
	x[1];

solve satisfy;


