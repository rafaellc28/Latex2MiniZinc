enum SOLDIER;

set of int: DAY = 1..nDays;

enum SHIFT = {OFF,EVE,NIGHT};

int: nDays;

int: o;

int: l;

int: u;


array[INDEX_SET_onEve_1] of var l..u: onEve;

array[INDEX_SET_roster_1, INDEX_SET_roster_2] of var SHIFT: roster;

set of int: INDEX_SET_onEve_1;

set of int: INDEX_SET_roster_1;

set of int: INDEX_SET_roster_2;


include "global_cardinality.mzn";

constraint forall(d in 1..(nDays - 2), s in SOLDIER)((roster[s,d] = NIGHT) /\ (roster[s,d + 1] = NIGHT) -> (roster[s,d + 2] != NIGHT));

constraint forall(d in 1..(nDays - 1), s in SOLDIER)((roster[s,d] = EVE) -> (roster[s,d + 1] != NIGHT));

constraint forall(d in DAY)(global_cardinality([roster[s,d] | s in SOLDIER],[NIGHT,EVE],[o,onEve[d]]));



solve maximize sum(onEve);




