set of int: MOVES = 1..nMoves;

array[MOVES] of 1..10: duration;

int: timeBound;

array[MOVES] of 1..20: power;

int: nMoves;


array[MOVES] of var int: occur;


constraint forall(i in MOVES)(occur[i] >= 0);

constraint forall(i in MOVES)(occur[i] <= 1);

constraint (sum(i in MOVES)(duration[i] * occur[i])) <= timeBound;



solve maximize sum(i in MOVES)(power[i] * occur[i]);




