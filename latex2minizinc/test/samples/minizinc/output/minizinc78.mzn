set of int: SPOT = 1..nSpot;

set of int: CLUSTER = 1..k;

array[SPOT, SPOT] of float: dist;

float: maxSep;

int: nSpot;

int: k;

float: maxdist = max([dist[i,j] | i,j in SPOT]);


var float: obj = min(i,j in SPOT where i < j)(if shot[i] = shot[j] then maxdist else dist[i,j] endif);

array[SPOT] of var CLUSTER: shot;


include "value_precede_chain.mzn";

constraint forall(i,j in SPOT where shot[i] = shot[j])(dist[i,j] <= maxSep);

constraint value_precede_chain([i | i in CLUSTER],shot);



solve maximize obj;




