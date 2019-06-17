set of int: PREC = 1..p;

enum TASK;

array[PREC, 1..2] of TASK: pre;

array[TASK] of int: duration;

int: t = sum(duration);

int: p;


var 0..t: makespan = max(t in TASK)(start[t] + duration[t]);

array[TASK] of var 0..t: start;


constraint forall(i in PREC)(start[pre[i,1]] + duration[pre[i,1]] <= start[pre[i,2]]);



solve minimize makespan;




