array[INDEX_SET_LINKS, 1..2] of DEST: LINKS;

enum ORIG;

enum DEST;

array[int, int] of float: cost;

array[ORIG] of float: supply;

array[DEST] of float: demand;


array[INDEX_SET_Trans_1, INDEX_SET_Trans_2] of var float: Trans;

set of int: INDEX_SET_LINKS;

set of int: INDEX_SET_Trans_1 = LINKS;

set of int: INDEX_SET_Trans_2;


constraint forall(l in INDEX_SET_LINKS)(assert(cost[LINKS[l,1],LINKS[l,2]] >= 0, "Assertion cost[\(LINKS[l,1]),\(LINKS[l,2])] >= 0 failed!"));

constraint forall(l in INDEX_SET_Trans_1, i0 in INDEX_SET_Trans_2)(Trans[l,i0] >= 0);

constraint forall(i in ORIG)(sum(i in INDEX_SET_LINKS)(Trans[LINKS[i,1],LINKS[i,2]]) = supply[i]);

constraint forall(j in DEST)(sum(i in INDEX_SET_LINKS)(Trans[LINKS[i,1],LINKS[i,2]]) = demand[j]);



solve minimize sum(i in INDEX_SET_LINKS)(cost[LINKS[i,1],LINKS[i,2]] * Trans[LINKS[i,1],LINKS[i,2]]);




