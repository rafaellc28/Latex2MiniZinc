array[INDEX_SET_TASKS, 1..2] of int: TASKS;

array[INDEX_SET_TASKORDER, 1..4] of int: TASKORDER;

array[int,int] of float: dur;

enum JOBS;

enum MACHINES;

float: BigM = 1 + sum(j in INDEX_SET_TASKS)(dur[TASKS[j,0],TASKS[j,1]]);

set of int: INDEX_SET_TASKS;

set of int: INDEX_SET_TASKORDER;


array[int,int,int] of var bool: y;

array[int,int] of var float: start;

var float: makespan;


constraint forall(i in INDEX_SET_TASKS)(start[TASKS[i,0],TASKS[i,1]] >= 0);

constraint makespan >= 0;

constraint forall(j in INDEX_SET_TASKS)(start[TASKS[j,0],TASKS[j,1]] + dur[TASKS[j,0],TASKS[j,1]] <= makespan);

constraint forall(k in INDEX_SET_TASKORDER)(start[TASKORDER[k,0],TASKORDER[k,1]] + dur[TASKORDER[k,0],TASKORDER[k,1]] <= start[TASKORDER[k,2],TASKORDER[k,3]]);

constraint forall(i in INDEX_SET_TASKS, j in INDEX_SET_TASKS where TASKS[i,0] < TASKS[j,0])(start[TASKS[i,0],TASKS[i,1]] + dur[TASKS[i,0],TASKS[i,1]] <= start[TASKS[j,0],TASKS[i,1]] + BigM * (1 - y[TASKS[i,0],TASKS[i,1],TASKS[j,0]]));

constraint forall(i in INDEX_SET_TASKS, j in INDEX_SET_TASKS where TASKS[i,0] < TASKS[j,0])(start[TASKS[j,0],TASKS[i,1]] + dur[TASKS[j,0],TASKS[i,1]] <= start[TASKS[i,0],TASKS[i,1]] + BigM * y[TASKS[i,0],TASKS[i,1],TASKS[j,0]]);



var float: obj = BigM * makespan + sum(j in INDEX_SET_TASKS)(start[TASKS[j,0],TASKS[j,1]]);

solve minimize obj;




