set of int: SHIP = 1..nS;

set of int: SHIPE = 1..floor(nS + nC);

set of int: TIME = 0..maxt;

int: maxt;

int: nS;

int: nC;

array[1..nC] of int: len;

array[SHIP] of int: speed;

array[SHIP] of enter..dummy: kind = dirn ++ [dummy | i in 1..nC];

int: leeway;

array[int] of int: speede = speed ++ [0 | i in 1..nC];

array[SHIP] of int: desired;

int: enter = 1;

int: leave = 2;

int: dummy = 3;

array[SHIP] of enter..leave: dirn;


array[SHIP] of var TIME: start;

array[SHIP] of var TIME: end;

array[SHIP] of var SHIPE: next;

array[SHIP] of var 1..nC: channel;


include "alldifferent.mzn";

constraint forall(s in floor(nS + 1)..floor(nS + nC))(start[s] = maxt /\ end[s] = maxt);

constraint forall(s in floor(nS + 1)..floor(nS + nC))(channel[s] = s - nS);

constraint forall(s in SHIP)(end[s] = start[s] + len[channel[s]] * speed[s]);

constraint alldifferent(next);

constraint forall(s in SHIP)(if kind[s] + kind[next[s]] = 3 then end[s] <= start[next[s]] else start[s] + speed[s] * leeway <= start[next[s]] /\ end[s] + speede[next[s]] * leeway <= end[next[s]] endif);

constraint forall(s in SHIP)(start[s] >= desired[s]);

constraint forall(s in SHIP)(channel[next[s]] = channel[s]);



solve minimize max(s in SHIP)(end[s]);




