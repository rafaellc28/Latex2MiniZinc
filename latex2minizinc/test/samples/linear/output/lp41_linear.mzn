array[INDEX_SET_ABILITIES, 1..2] of PROJECTS: ABILITIES;

set of int: PEOPLE;

set of int: PROJECTS;

array[int, int] of float: cost;

array[int] of float: supply;

array[int] of float: demand;

array[int, int] of float: limit;


array[INDEX_SET_Assign_1, INDEX_SET_Assign_2] of var float: Assign;

set of int: INDEX_SET_ABILITIES;

set of int: INDEX_SET_Assign_1 = ABILITIES;

set of int: INDEX_SET_Assign_2;


constraint forall(i in INDEX_SET_ABILITIES)(assert(cost[ABILITIES[i,1],ABILITIES[i,2]] >= 0, "Assertion cost[\(ABILITIES[i,1]),\(ABILITIES[i,2])] >= 0 failed!"));

constraint forall(p in PEOPLE)(assert(supply[p] >= 0, "Assertion supply[\(p)] >= 0 failed!"));

constraint forall(pr in PROJECTS)(assert(demand[pr] >= 0, "Assertion demand[\(pr)] >= 0 failed!"));

constraint forall(i in INDEX_SET_ABILITIES)(assert(limit[ABILITIES[i,1],ABILITIES[i,2]] >= 0, "Assertion limit[\(ABILITIES[i,1]),\(ABILITIES[i,2])] >= 0 failed!"));

constraint forall(i in INDEX_SET_ABILITIES)(Assign[ABILITIES[i,1],ABILITIES[i,2]] <= limit[ABILITIES[i,1],ABILITIES[i,2]] /\ Assign[ABILITIES[i,1],ABILITIES[i,2]] >= 0);

constraint forall(i in PEOPLE)(sum(i in INDEX_SET_ABILITIES)(Assign[ABILITIES[i,1],ABILITIES[i,2]]) = supply[i]);

constraint forall(j in PROJECTS)(sum(i in INDEX_SET_ABILITIES)(Assign[ABILITIES[i,1],ABILITIES[i,2]]) = demand[j]);



solve minimize sum(i in INDEX_SET_ABILITIES)(cost[ABILITIES[i,1],ABILITIES[i,2]] * Assign[ABILITIES[i,1],ABILITIES[i,2]]);




