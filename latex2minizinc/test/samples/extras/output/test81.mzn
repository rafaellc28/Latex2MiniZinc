float: y;


constraint let {var int: x; constraint x >= y /\ x >= -y /\ (x = y \/ x = -y)} in
	x;

solve satisfy;


