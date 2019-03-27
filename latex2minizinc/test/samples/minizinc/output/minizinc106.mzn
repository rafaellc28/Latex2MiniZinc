var -1..7: u;


predicate even(var int: x) =
	let {var int: y} in
	x = 2 * y;

constraint not even(u);

solve satisfy;


