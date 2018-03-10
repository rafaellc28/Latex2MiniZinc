set of int: ESSTANZA = 1..floor(k + l);

set of int: POSN = 1..n;

set of int: STANZA = 0..floor(k + l);

enum KIND = {E,S,O};

int: other = 0;

int: n = k + l + m;

array[int] of KIND: kind = [E | i in 1..k] ++ [S | i in 1..l];

int: k;

int: l;

int: m;

array[int] of int: effect;


array[INDEX_SET_place_1] of var POSN: place;

array[INDEX_SET_what_1] of var STANZA: what;

var int: obj = sum(p in 1..floor(n - 1))(if what[p] != other /\ what[p + 1] != other then abs(effect[what[p]] - effect[what[p + 1]]) else 0 endif);

set of int: INDEX_SET_place_1;

set of int: INDEX_SET_what_1;


include "alldifferent.mzn";

constraint what[1] != other /\ forall(i in 1..floor(n - 1))(what[i] = other /\ what[i + 1] = other -> forall(j in i..n)(what[j] = other));

constraint forall(i in ESSTANZA, j in POSN)(place[i] = j <-> what[j] = i);

constraint alldifferent(place);

constraint forall(p1,p2 in ESSTANZA where p1 < p2)(kind[p1] = kind[p2] -> abs(place[p1] - place[p2]) > 1);



solve maximize obj;




