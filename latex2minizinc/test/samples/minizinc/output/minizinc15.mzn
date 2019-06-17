array[INDEX_SET_group] of set of int: group;

enum SYMB;

set of int: SPOT = 1..nSpots;

int: size;

array[int] of int: damage;

int: nSpots;


var int: totalDamages = sum(p in attacks)(damage[p]);

array[1..size] of var SPOT: attacks;

set of int: INDEX_SET_group;


constraint forall(s in SYMB)(sum(i in 1..size)(attacks[i] in group[s]) <= 1);

constraint forall(i in 1..floor(size - 1))(attacks[i] < attacks[i + 1]);



solve maximize (totalDamages);




