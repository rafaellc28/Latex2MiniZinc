array[INDEX_SET_PAIRS, 1..2] of TASKS: PAIRS;

enum TASKS;

array[1..M, 1..M] of float: Saving;

int: M;


array[TASKS, TASKS] of var bool: before;

set of int: INDEX_SET_PAIRS;


constraint forall(a in TASKS, b in TASKS, c in TASKS where a < b /\ a < c /\ c < b)(before[a,b] - before[c,b] - before[a,c] <= 0);

constraint forall(a in TASKS, b in TASKS, c in TASKS where a < b /\ a < c /\ b < c)(before[a,b] + before[b,c] - before[a,c] <= 1);

constraint forall(d in 1..M, e in 1..M)(Saving[d,e] >= 0);



solve maximize sum(a in INDEX_SET_PAIRS)((Saving[PAIRS[a,1],PAIRS[a,2]] * before[PAIRS[a,1],PAIRS[a,2]] + Saving[PAIRS[a,2],PAIRS[a,1]] * (1 - before[PAIRS[a,1],PAIRS[a,2]])));




