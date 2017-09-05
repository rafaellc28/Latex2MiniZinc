enum cities;

array[INDEX_SET_schedule, 1..4] of int: schedule;

enum times;

array[INDEX_SET_Links, 1..2] of int: Links;

times: Last;

array[int, int] of float: Distance;

array[int, int, int, int] of float: Low;

array[int, int, int, int] of float: High;

set of int: INDEX_SET_Links;

set of int: INDEX_SET_schedule;


array[int, int, int, int] of var float: X;

array[int, int] of var float: U;


constraint forall(c1 in INDEX_SET_schedule)(X[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] >= 0);

constraint forall(c in cities, t in times)(U[c,t] >= 0);

constraint forall(c in cities, t in times)(U[c,t] = U[c,if t > 1 then t - 1 else Last endif] + sum(c1 in INDEX_SET_schedule)(X[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] - sum(c in INDEX_SET_schedule)(X[schedule[c,1],schedule[c,2],schedule[c,3],schedule[c,4]])));

constraint forall(c1 in INDEX_SET_schedule)(X[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] <= High[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] /\ X[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]] >= Low[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]]);

constraint forall(c1 in INDEX_SET_Links)(Distance[Links[c1,1],Links[c1,2]] >= 0);



var float: obj = sum(c in cities)(U[c,Last] + sum(c1 in INDEX_SET_schedule where schedule[c1,4] < schedule[c1,2])(X[schedule[c1,1],schedule[c1,2],schedule[c1,3],schedule[c1,4]]));

solve minimize obj;




