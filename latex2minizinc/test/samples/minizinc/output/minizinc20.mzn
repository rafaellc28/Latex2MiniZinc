set of int: MOVES = 1..nMoves;

array[int] of 1..10: duration;

int: timeBound;

array[int] of 1..20: power;

int: nMoves;


array[INDEX_SET_occur_1] of var 0..1: occur;

set of int: INDEX_SET_occur_1;


constraint (sum(i in MOVES)(duration[i] * occur[i])) <= timeBound;



solve maximize sum(i in MOVES)(power[i] * occur[i]);




