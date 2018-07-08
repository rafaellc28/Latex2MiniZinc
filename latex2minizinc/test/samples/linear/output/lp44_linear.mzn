enum cities;

array[INDEX_SET_schedule, 1..4] of int: schedule;

enum times;

array[int, int] of float: U;

array[int, int, int, int] of float: X;

int: last;

array[int, int, int, int] of float: demand;

int: section;

set of int: INDEX_SET_schedule;


constraint forall(c in cities, t in times)(U[c,t] = U[c,if t > 1 then t - 1 else last endif] + sum(c1 in INDEX_SET_schedule)(X[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] - sum(c in INDEX_SET_schedule)(X[schedule[c,1],schedule[c,2],schedule[c,3],schedule[c,4]])));

constraint forall(c1 in INDEX_SET_schedule)(X[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] <= section * ceil(demand[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]]/section) /\ X[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] >= demand[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]]);

constraint forall(c1 in INDEX_SET_schedule)(demand[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] > 0);



solve minimize sum(c in cities)(U[c,last] + sum(c1 in INDEX_SET_schedule where schedule[c1,4] < schedule[c1,2])(X[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]]));




