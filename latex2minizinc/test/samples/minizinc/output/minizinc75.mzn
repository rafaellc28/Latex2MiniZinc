set of int: DAY = 1..nDays;

enum SOLDIER;

enum SHIFT = {OFF,EVE,NIGHT};

int: o;

int: l;

int: u;

int: nDays;


var int: tOnEve = sum(d in DAY)(onEve[d]);

array[DAY] of var l..u: onEve;

array[SHIFT, DAY] of var set of SOLDIER: rosterShift;

array[SOLDIER, DAY] of var SHIFT: rosterSoldier;


include "global_cardinality.mzn";

include "int_set_channel.mzn";

constraint forall(d in DAY)(card(rosterShift[NIGHT,d]) = o);

constraint forall(d in DAY)(card(rosterShift[EVE,d]) >= l);

constraint forall(d in DAY)(card(rosterShift[EVE,d]) <= u);

constraint forall(d in DAY)(rosterShift[OFF,d] union rosterShift[EVE,d] union rosterShift[NIGHT,d] = SOLDIER);

constraint forall(d in DAY)(rosterShift[OFF,d] intersect rosterShift[EVE,d] = {});

constraint forall(d in DAY)(rosterShift[OFF,d] intersect rosterShift[NIGHT,d] = {});

constraint forall(d in DAY)(rosterShift[EVE,d] intersect rosterShift[NIGHT,d] = {});

constraint forall(d in 1..(nDays - 1), s in SOLDIER)((s in rosterShift[EVE,d]) -> (not (s in rosterShift[NIGHT,d + 1])));

constraint forall(d in 1..(nDays - 2), s in SOLDIER)((s in rosterShift[NIGHT,d]) /\ (s in rosterShift[NIGHT,d + 1]) -> (not (s in rosterShift[NIGHT,d + 2])));

constraint forall(d in DAY)(global_cardinality([rosterSoldier[s,d] | s in SOLDIER],[NIGHT,EVE],[o,onEve[d]]));

constraint forall(d in 1..(nDays - 1), s in SOLDIER)((rosterSoldier[s,d] = EVE) -> (rosterSoldier[s,d + 1] != NIGHT));

constraint forall(d in 1..(nDays - 2), s in SOLDIER)((rosterSoldier[s,d] = NIGHT) /\ (rosterSoldier[s,d + 1] = NIGHT) -> (rosterSoldier[s,d + 2] != NIGHT));

constraint forall(d in DAY)(int_set_channel([rosterSoldier[so,d] | so in SOLDIER],[rosterShift[sh,d] | sh in SHIFT]));



solve maximize (tOnEve);




