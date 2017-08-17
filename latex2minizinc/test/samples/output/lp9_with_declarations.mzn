int: M;

enum TASKS;

array[1..M, 1..M] of float: saving;

array[INDEX_SET_TASKS, 1..2] of TASKS: PAIRS;

set of int: INDEX_SET_TASKS = index_set(TASKS);


array[TASKS, TASKS] of var bool: before;


constraint forall(a in TASKS, b in TASKS, c in TASKS where a < b /\ a < c /\ c < b)(before[a,b] - before[c,b] - before[a,c] <= 0);

constraint forall(a in TASKS, b in TASKS, c in TASKS where a < b /\ a < c /\ b < c)(before[a,b] + before[b,c] - before[a,c] <= 1);



var float: obj = sum(a in INDEX_SET_TASKS)((saving[PAIRS[a,0],PAIRS[a,1]] * before[PAIRS[a,0],PAIRS[a,1]] + saving[PAIRS[a,1],PAIRS[a,0]] * (1 - before[PAIRS[a,0],PAIRS[a,1]])));

solve maximize obj;




