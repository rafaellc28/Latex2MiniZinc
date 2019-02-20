int: s = 1;

int: e = 10;


var s..e: x;


constraint let {int: l = s div 2; int: u = e div 2; var l..u: y} in
	x = 2 * y;

solve satisfy;


