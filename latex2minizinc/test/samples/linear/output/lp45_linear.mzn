enum cities;

array[INDEX_SET_schedule, 1..4] of int: schedule;

set of int: times = 1..last;

array[INDEX_SET_links, 1..2] of int: links;

int: last;

array[INDEX_SET_low_1, INDEX_SET_low_2, INDEX_SET_low_3, INDEX_SET_low_4] of float: low = array4d(INDEX_SET_low_1, INDEX_SET_low_2, INDEX_SET_low_3, INDEX_SET_low_4, [ceil(demand[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]]) | c1 in INDEX_SET_schedule]);

array[INDEX_SET_high_1, INDEX_SET_high_2, INDEX_SET_high_3, INDEX_SET_high_4] of float: high = array4d(INDEX_SET_high_1, INDEX_SET_high_2, INDEX_SET_high_3, INDEX_SET_high_4, [max(2,min(ceil(2 * demand[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]]),section * ceil(demand[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] / section))) | c1 in INDEX_SET_schedule]);

int: section;

array[int, int, int, int] of float: demand;

array[int, int] of float: distance;

array[int, int] of float: dist_table;


array[INDEX_SET_U_1, INDEX_SET_U_2] of var float: U;

array[INDEX_SET_X_1, INDEX_SET_X_2, INDEX_SET_X_3, INDEX_SET_X_4] of var float: X;

set of int: INDEX_SET_U_1 = cities;

set of int: INDEX_SET_U_2 = times;

set of int: INDEX_SET_X_1 = schedule;

set of int: INDEX_SET_X_2;

set of int: INDEX_SET_X_3;

set of int: INDEX_SET_X_4;

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

constraint forall(s in INDEX_SET_schedule)(assert(demand[schedule[s,1],schedule[s,2],schedule[s,3],schedule[s,4]] > 0, "Assertion demand[\(schedule[s,1]),\(schedule[s,2]),\(schedule[s,3]),\(schedule[s,4])] > 0 failed!"));

constraint forall(c1 in INDEX_SET_links)(assert(distance[links[c1,1],links[c1,2]] > 0, "Assertion distance[\(links[c1,1]),\(links[c1,2])] > 0 failed!"));

constraint forall(l in INDEX_SET_links)(assert(dist_table[links[l,1],links[l,2]] >= 0, "Assertion dist_table[\(links[l,1]),\(links[l,2])] >= 0 failed!"));

constraint forall(c in INDEX_SET_U_1, t in INDEX_SET_U_2)(U[c,t] >= 0);

constraint forall(s in INDEX_SET_X_1, i0 in INDEX_SET_X_2, i1 in INDEX_SET_X_3, i2 in INDEX_SET_X_4)(X[s,i0,i1,i2] >= 0);

constraint forall(c in cities, t in times)(U[c,t] = U[c,if t > 1 then t - 1 else last endif] + sum(c1 in INDEX_SET_schedule)(X[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] - sum(c in INDEX_SET_schedule)(X[schedule[c,1],schedule[c,2],schedule[c,3],schedule[c,4]])));

constraint forall(c1 in INDEX_SET_schedule)(X[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] <= high[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] /\ X[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] >= low[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]]);



solve minimize sum(c in cities)(U[c,last] + sum(c1 in INDEX_SET_schedule where schedule[c1,4] < schedule[c1,2])(X[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]]));




