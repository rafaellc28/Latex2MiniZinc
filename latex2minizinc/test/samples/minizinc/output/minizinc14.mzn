array[SYMB] of set of SPOT: group;

enum SYMB;

set of int: SPOT = 1..nSpots;

array[int] of int: damage;

int: nSpots;


var int: totalDamages = sum(p in attacks)(damage[p]);

var set of SPOT: attacks;


constraint forall(s in SYMB)(card(attacks intersect group[s]) <= 1);



solve maximize (totalDamages);




