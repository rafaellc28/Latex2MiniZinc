set of int: SHIP = 1..nS;

set of int: SHIPE = 1..floor(nS + 1);

set of int: TIME = 0..maxt;

int: nS;

int: maxt;

float: len;

array[SHIP] of int: speed;

array[SHIP] of enter..dummy: kind = dirn ++ [dummy];

int: leeway;

array[int] of int: speede = speed ++ [0];

array[SHIP] of int: desired;

int: enter = 1;

int: leave = 2;

int: dummy = 3;

array[SHIP] of enter..leave: dirn;


array[SHIP] of var TIME: start;

array[SHIP] of var TIME: end;

array[SHIP] of var SHIPE: next;


include "alldifferent.mzn";

constraint start[nS + 1] = maxt;

constraint end[nS + 1] = maxt;

constraint forall(s in SHIP)(end[s] = start[s] + len * speed[s]);

constraint alldifferent(next);

constraint forall(s in SHIP)(if kind[s] + kind[next[s]] = 3 then end[s] <= start[next[s]] else start[s] + speed[s] * leeway <= start[next[s]] /\ end[s] + speede[next[s]] * leeway <= end[next[s]] endif);

constraint forall(s in SHIP)(start[s] >= desired[s]);



solve minimize max(s in SHIP)(end[s]);




