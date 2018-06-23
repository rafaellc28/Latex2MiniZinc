set of int: MOVES = 1..nMoves;

array[int] of 1..10: duration;

int: timeBound;

array[int] of 1..20: power;

int: nMoves;


array[INDEX_SET_occur_1] of var int: occur;

set of int: INDEX_SET_occur_1 = MOVES;


constraint forall(i in MOVES)(occur[i] >= 0);

constraint forall(i in MOVES)(occur[i] <= 1);

constraint (sum(i in MOVES)(duration[i] * occur[i])) <= timeBound;



solve maximize sum(i in MOVES)(power[i] * occur[i]);




