set of int: PREC = 1..p;

enum TASK;

enum RESOURCE;

array[PREC, 1..2] of TASK: pre;

array[TASK] of int: duration;

array[RESOURCE, TASK] of int: res;

array[RESOURCE] of int: L;

int: t = sum(duration);

int: p;


var int: makespan = max(t in TASK)(start[t] + duration[t]);

array[TASK] of var 0..t: start;


include "cumulative.mzn";

constraint forall(i in PREC)(start[pre[i,1]] + duration[pre[i,1]] <= start[pre[i,2]]);

constraint forall(r in RESOURCE)(cumulative(start,duration,[res[r,t] | t in TASK],L[r]));



solve minimize makespan;




