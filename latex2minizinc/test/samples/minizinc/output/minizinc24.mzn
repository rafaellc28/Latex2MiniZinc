set of int: MOVES = 1..nMoves;

array[MOVES] of 1..10: duration;

int: timeBound;

array[MOVES] of 1..20: power;

int: nMoves;


var set of MOVES: occur;


constraint (sum(i in occur)(duration[i])) <= timeBound;



solve maximize sum(i in occur)(power[i]);




