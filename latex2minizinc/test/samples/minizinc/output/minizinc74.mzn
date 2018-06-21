set of int: DAY = 1..nDays;

enum SOLDIER;

enum SHIFT = {OFF,EVE,NIGHT};

int: o;

int: l;

int: u;

int: nDays;


var int: tOnEve = sum(d in DAY)(card(roster[EVE,d]));

array[INDEX_SET_roster_1, INDEX_SET_roster_2] of var set of SOLDIER: roster;

set of int: INDEX_SET_roster_1;

set of int: INDEX_SET_roster_2;


constraint forall(d in DAY)(card(roster[NIGHT,d]) = o);

constraint forall(d in DAY)(card(roster[EVE,d]) >= l);

constraint forall(d in DAY)(card(roster[EVE,d]) <= u);

constraint forall(d in DAY)(roster[OFF,d] union roster[EVE,d] union roster[NIGHT,d] = SOLDIER);

constraint forall(d in DAY)(roster[OFF,d] intersect roster[EVE,d] = {});

constraint forall(d in DAY)(roster[OFF,d] intersect roster[NIGHT,d] = {});

constraint forall(d in DAY)(roster[EVE,d] intersect roster[NIGHT,d] = {});

constraint forall(d in 1..(nDays - 1), s in SOLDIER)((s in roster[EVE,d]) -> (not (s in roster[NIGHT,d + 1])));

constraint forall(d in 1..(nDays - 2), s in SOLDIER)((s in roster[NIGHT,d]) /\ (s in roster[NIGHT,d + 1]) -> (not (s in roster[NIGHT,d + 2])));



solve maximize (tOnEve);




