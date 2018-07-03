array[INDEX_SET_LINKS, 1..2] of CITIES: LINKS;

set of int: CITIES;

array[int, int] of float: cost;

array[int, int] of float: Ship;

array[int] of float: supply;

array[int] of float: demand;

array[int] of float: demmand;

array[int, int] of float: capacity;

set of int: INDEX_SET_LINKS;


constraint forall(i in INDEX_SET_LINKS)(assert(cost[LINKS[i,1],LINKS[i,2]] >= 0, "Assertion cost[\(LINKS[i,1]),\(LINKS[i,2])] >= 0 failed!"));

constraint forall(i in INDEX_SET_LINKS)(assert(Ship[LINKS[i,1],LINKS[i,2]] <= capacity[LINKS[i,1],LINKS[i,2]] /\ Ship[LINKS[i,1],LINKS[i,2]] >= 0, "Assertion Ship[\(LINKS[i,1]),\(LINKS[i,2])] <= capacity[\(LINKS[i,1]),\(LINKS[i,2])] /\\ Ship[\(LINKS[i,1]),\(LINKS[i,2])] >= 0 failed!"));

constraint forall(c in CITIES)(assert(supply[c] >= 0, "Assertion supply[\(c)] >= 0 failed!"));

constraint forall(c in CITIES)(assert(demmand[c] >= 0, "Assertion demmand[\(c)] >= 0 failed!"));

constraint forall(i in INDEX_SET_LINKS)(assert(capacity[LINKS[i,1],LINKS[i,2]] >= 0, "Assertion capacity[\(LINKS[i,1]),\(LINKS[i,2])] >= 0 failed!"));

constraint forall(k in CITIES)(supply[k] + sum(i in INDEX_SET_LINKS)(Ship[LINKS[i,1],LINKS[i,2]]) = demand[k] + sum(k in INDEX_SET_LINKS)(Ship[LINKS[k,1],LINKS[k,2]]));



solve minimize sum(i in INDEX_SET_LINKS)(cost[LINKS[i,1],LINKS[i,2]] * Ship[LINKS[i,1],LINKS[i,2]]);




