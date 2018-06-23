array[INDEX_SET_PAIRS, 1..2] of TASKS: PAIRS;

set of int: TASKS = 1..M;

array[int, int] of float: saving;

int: M;


array[INDEX_SET_before_1, INDEX_SET_before_2] of var bool: before;

set of int: INDEX_SET_PAIRS;

set of int: INDEX_SET_before_1 = TASKS;

set of int: INDEX_SET_before_2 = TASKS;


constraint forall(a in TASKS, b in TASKS, c in TASKS where a < b /\ a < c /\ c < b)(before[a,b] - before[c,b] - before[a,c] <= 0);

constraint forall(a in TASKS, b in TASKS, c in TASKS where a < b /\ a < c /\ b < c)(before[a,b] + before[b,c] - before[a,c] <= 1);



solve maximize sum(a in INDEX_SET_PAIRS)((saving[PAIRS[a,1],PAIRS[a,2]] * before[PAIRS[a,1],PAIRS[a,2]] + saving[PAIRS[a,2],PAIRS[a,1]] * (1 - before[PAIRS[a,1],PAIRS[a,2]])));




