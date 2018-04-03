enum SOLDIER;

set of int: DAY = 1..nDays;

enum SHIFT = {OFF,EVE,NIGHT};

int: nDays;

int: o;

int: l;

int: u;


var int: tOnEve = sum(d in DAY)(sum(s in SOLDIER)(roster[s,d] = EVE));

array[INDEX_SET_roster_1, INDEX_SET_roster_2] of var SHIFT: roster;

set of int: INDEX_SET_roster_1;

set of int: INDEX_SET_roster_2;


constraint forall(d in 1..(nDays - 2), s in SOLDIER)((roster[s,d] = NIGHT) /\ (roster[s,d + 1] = NIGHT) -> (roster[s,d + 2] != NIGHT));

constraint forall(d in 1..(nDays - 1), s in SOLDIER)((roster[s,d] = EVE) -> (roster[s,d + 1] != NIGHT));

constraint forall(d in DAY)(sum(s in SOLDIER)(roster[s,d] = NIGHT) = o);

constraint forall(d in DAY)(sum(s in SOLDIER)(roster[s,d] = EVE) >= l);

constraint forall(d in DAY)(sum(s in SOLDIER)(roster[s,d] = EVE) <= u);



solve maximize tOnEve;




