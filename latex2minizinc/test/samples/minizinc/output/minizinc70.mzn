enum SOLDIER;

set of int: DAY = 1..nDays;

enum SHIFT = {OFF,EVE,NIGHT};

int: nDays;

int: o;

int: l;

int: u;


array[DAY] of var l..u: onEve;

array[SOLDIER, DAY] of var SHIFT: roster;


include "global_cardinality.mzn";

constraint forall(d in 1..(nDays - 2), s in SOLDIER)((roster[s,d] = NIGHT) /\ (roster[s,d + 1] = NIGHT) -> (roster[s,d + 2] != NIGHT));

constraint forall(d in 1..(nDays - 1), s in SOLDIER)((roster[s,d] = EVE) -> (roster[s,d + 1] != NIGHT));

constraint forall(d in DAY)(global_cardinality([roster[s,d] | s in SOLDIER],[NIGHT,EVE],[o,onEve[d]]));



solve maximize sum(onEve);




