array[INDEX_SET_TASKS, 1..2] of int: TASKS;

array[INDEX_SET_TASKORDER, 1..4] of int: TASKORDER;

float: BigM;

array[int, int] of float: Dur;

set of int: INDEX_SET_TASKORDER;

set of int: INDEX_SET_TASKS;


array[int, int] of var float: start;

var float: makespan;

array[int, int, int] of var bool: y;


constraint forall(i in INDEX_SET_TASKS)(start[TASKS[i,1],TASKS[i,2]] >= 0);

constraint makespan >= 0;

constraint forall(j in INDEX_SET_TASKS)(start[TASKS[j,1],TASKS[j,2]] + Dur[TASKS[j,1],TASKS[j,2]] <= makespan);

constraint forall(k in INDEX_SET_TASKORDER)(start[TASKORDER[k,1],TASKORDER[k,2]] + Dur[TASKORDER[k,1],TASKORDER[k,2]] <= start[TASKORDER[k,3],TASKORDER[k,4]]);

constraint forall(i in INDEX_SET_TASKS, j in INDEX_SET_TASKS where TASKS[i,1] < TASKS[j,1])(start[TASKS[i,1],TASKS[i,2]] + Dur[TASKS[i,1],TASKS[i,2]] <= start[TASKS[j,1],TASKS[i,2]] + BigM * (1 - y[TASKS[i,1],TASKS[i,2],TASKS[j,1]]));

constraint forall(i in INDEX_SET_TASKS, j in INDEX_SET_TASKS where TASKS[i,1] < TASKS[j,1])(start[TASKS[j,1],TASKS[i,2]] + Dur[TASKS[j,1],TASKS[i,2]] <= start[TASKS[i,1],TASKS[i,2]] + BigM * y[TASKS[i,1],TASKS[i,2],TASKS[j,1]]);



var float: obj = BigM * makespan + sum(j in INDEX_SET_TASKS)(start[TASKS[j,1],TASKS[j,2]]);

solve minimize obj;




