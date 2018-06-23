enum cities;

array[INDEX_SET_schedule, 1..4] of int: schedule;

enum times;

array[INDEX_SET_Links, 1..2] of int: Links;

int: Last;

array[int, int] of float: Distance;

array[int, int, int, int] of float: Low;

array[int, int, int, int] of float: High;


array[INDEX_SET_X_1, INDEX_SET_X_2, INDEX_SET_X_3, INDEX_SET_X_4] of var float: X;

array[INDEX_SET_U_1, INDEX_SET_U_2] of var float: U;

set of int: INDEX_SET_Links;

set of int: INDEX_SET_U_1 = cities;

set of int: INDEX_SET_U_2 = times;

set of int: INDEX_SET_X_1 = schedule;

set of int: INDEX_SET_X_2;

set of int: INDEX_SET_X_3;

set of int: INDEX_SET_X_4;

set of int: INDEX_SET_schedule;


constraint forall(c1 in INDEX_SET_schedule)(X[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] >= 0);

constraint forall(c in INDEX_SET_U_1, t in INDEX_SET_U_2)(U[c,t] >= 0);

constraint forall(c in cities, t in times)(U[c,t] = U[c,if t > 1 then t - 1 else Last endif] + sum(c1 in INDEX_SET_schedule)(X[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] - sum(c in INDEX_SET_schedule)(X[schedule[c,1],schedule[c,2],schedule[c,3],schedule[c,4]])));

constraint forall(c1 in INDEX_SET_schedule)(X[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] <= High[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] /\ X[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] >= Low[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]]);

constraint forall(c1 in INDEX_SET_Links)(Distance[Links[c1,1],Links[c1,2]] >= 0);



solve minimize sum(c in cities)(U[c,Last] + sum(c1 in INDEX_SET_schedule where schedule[c1,4] < schedule[c1,2])(X[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]]));




