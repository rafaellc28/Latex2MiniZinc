set of int: SHIP = 1..nS;

set of int: SHIPE = 1..floor(nS + nC);

set of int: TIME = 0..maxt;

int: maxt;

int: nS;

int: nC;

array[int] of int: len;

array[int] of int: speed;

array[int] of enter..dummy: kind = dirn ++ [dummy | i in 1..nC];

int: leeway;

array[int] of int: speede = speed ++ [0 | i in 1..nC];

array[int] of int: desired;

int: enter = 1;

int: leave = 2;

int: dummy = 3;

array[int] of enter..leave: dirn;


array[INDEX_SET_start_1] of var TIME: start;

array[INDEX_SET_end_1] of var TIME: end;

array[INDEX_SET_next_1] of var SHIPE: next;

array[INDEX_SET_channel_1] of var 1..nC: channel;

set of int: INDEX_SET_channel_1 = SHIP;

set of int: INDEX_SET_end_1 = SHIP;

set of int: INDEX_SET_next_1 = SHIP;

set of int: INDEX_SET_start_1 = SHIP;


include "alldifferent.mzn";

constraint forall(s in floor(nS + 1)..floor(nS + nC))(start[s] = maxt /\ end[s] = maxt);

constraint forall(s in floor(nS + 1)..floor(nS + nC))(channel[s] = s - nS);

constraint forall(s in SHIP)(end[s] = start[s] + len[channel[s]] * speed[s]);

constraint alldifferent(next);

constraint forall(s in SHIP)(if kind[s] + kind[next[s]] = 3 then end[s] <= start[next[s]] else start[s] + speed[s] * leeway <= start[next[s]] /\ end[s] + speede[next[s]] * leeway <= end[next[s]] endif);

constraint forall(s in SHIP)(start[s] >= desired[s]);

constraint forall(s in SHIP)(channel[next[s]] = channel[s]);



solve minimize max(s in SHIP)(end[s]);




