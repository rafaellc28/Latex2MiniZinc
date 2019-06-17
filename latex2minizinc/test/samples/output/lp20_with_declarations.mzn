enum cities;

array[INDEX_SET_schedule, 1..4] of int: schedule;

set of int: times = 1..last;

array[INDEX_SET_links, 1..2] of int: links;

array[INDEX_SET_distance_1, INDEX_SET_distance_2] of float: distance = array2d(INDEX_SET_distance_1, INDEX_SET_distance_2, [if disttable[links[c1,1],links[c1,2]] > 0 then disttable[links[c1,1],links[c1,2]] else disttable[links[c1,2],links[c1,1]] endif | c1 in INDEX_SET_links]);

int: last;

array[INDEX_SET_low_1, INDEX_SET_low_2, INDEX_SET_low_3, INDEX_SET_low_4] of float: low = array4d(INDEX_SET_low_1, INDEX_SET_low_2, INDEX_SET_low_3, INDEX_SET_low_4, [ceil(demand[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]]) | c1 in INDEX_SET_schedule]);

array[INDEX_SET_high_1, INDEX_SET_high_2, INDEX_SET_high_3, INDEX_SET_high_4] of float: high = array4d(INDEX_SET_high_1, INDEX_SET_high_2, INDEX_SET_high_3, INDEX_SET_high_4, [max(2,min(ceil(2 * demand[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]]),section * ceil(demand[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] / section))) | c1 in INDEX_SET_schedule]);

int: section;

array[int, int, int, int] of float: demand;

array[int, int] of float: disttable;


array[cities, times] of var float: U;

array[INDEX_SET_X_1, INDEX_SET_X_2, INDEX_SET_X_3, INDEX_SET_X_4] of var float: X;

set of int: INDEX_SET_X_1 = schedule;

set of int: INDEX_SET_X_2;

set of int: INDEX_SET_X_3;

set of int: INDEX_SET_X_4;

set of int: INDEX_SET_distance_1;

set of int: INDEX_SET_distance_2;

set of int: INDEX_SET_high_1;

set of int: INDEX_SET_high_2;

set of int: INDEX_SET_high_3;

set of int: INDEX_SET_high_4;

set of int: INDEX_SET_links;

set of int: INDEX_SET_low_1;

set of int: INDEX_SET_low_2;

set of int: INDEX_SET_low_3;

set of int: INDEX_SET_low_4;

set of int: INDEX_SET_schedule;


constraint assert(last > 0, "Assertion last > 0 failed!");

constraint assert(section > 0, "Assertion section > 0 failed!");

constraint forall(c1 in INDEX_SET_schedule)(assert(demand[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] > 0, "Assertion demand[\(schedule[c1,1]),\(schedule[c1,2]),\(schedule[c1,3]),\(schedule[c1,4])] > 0 failed!"));

constraint forall(l1 in INDEX_SET_links)(assert(disttable[links[l1,1],links[l1,2]] >= 0, "Assertion disttable[\(links[l1,1]),\(links[l1,2])] >= 0 failed!"));

constraint forall(c in cities, t in times)(U[c,t] >= 0);

constraint forall(c1 in INDEX_SET_schedule)(X[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] >= 0);

constraint forall(c in cities, t in times)(U[c,t] = U[c,if t > 1 then t - 1 else last endif] + sum(c1 in INDEX_SET_schedule)(X[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] - sum(c in INDEX_SET_schedule)(X[schedule[c,1],schedule[c,2],schedule[c,3],schedule[c,4]])));

constraint forall(c1 in INDEX_SET_schedule)(X[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] <= high[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] /\ X[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] >= low[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]]);



solve minimize sum(c in cities)(U[c,last] + sum(c1 in INDEX_SET_schedule where schedule[c1,4] < schedule[c1,2])(X[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]]));




