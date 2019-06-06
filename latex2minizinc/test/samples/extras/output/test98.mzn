enum I;

enum J;


constraint let {array[int] of var int: y = [i | i in I where not(i in J)]; array[int] of var int: x} in
	x[1];

solve satisfy;


