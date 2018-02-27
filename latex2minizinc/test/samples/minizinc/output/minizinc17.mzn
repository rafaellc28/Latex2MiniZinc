array[INDEX_SET_group] of set of int: group;

enum SYMB;

set of int: SPOT = 1..nSpots;

set of int: SPOTx = {0} union SPOT;

int: size;

array[int] of int: damage;

int: nSpots;


var int: totalDamages = sum(p in attacks where p > 0)(damage[p]);

array[INDEX_SET_attacks_1] of var 0..nSpots: attacks;

set of int: INDEX_SET_attacks_1 = 1..size;

set of int: INDEX_SET_group;


constraint forall(s in SYMB)(sum(i in 1..size)(attacks[i] in group[s]) <= 1);

constraint forall(i in 1..floor(size - 1))(attacks[i] >= (attacks[i] != 0) + attacks[i + 1]);



solve maximize (totalDamages);




