array[INDEX_SET_a_1] of var 0..25: a;

set of int: INDEX_SET_a_1 = 1..2;


constraint not (8 >= sum(i in 1..2)(sqrt(a[i])));

function var int: sqrt(var int: x) =
	let {var int: y; constraint y * y = x /\ y >= 0} in
	y;

solve satisfy;


