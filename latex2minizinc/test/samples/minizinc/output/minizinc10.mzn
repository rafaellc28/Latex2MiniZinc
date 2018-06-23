set of int: PREC = 1..p;

enum TASK;

array[int, int] of TASK: pre;

array[int] of int: duration;

int: t = sum(duration);

int: p;


var 0..t: makespan = max(t in TASK)(start[t] + duration[t]);

array[INDEX_SET_start_1] of var 0..t: start;

set of int: INDEX_SET_start_1 = TASK;


constraint forall(i in PREC)(start[pre[i,1]] + duration[pre[i,1]] <= start[pre[i,2]]);



solve minimize makespan;




