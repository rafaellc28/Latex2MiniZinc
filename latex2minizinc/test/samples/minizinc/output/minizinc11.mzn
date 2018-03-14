set of int: PREC = 1..p;

enum TASK;

enum RESOURCE;

array[int, int] of TASK: pre;

array[int] of int: duration;

array[int, int] of int: res;

array[int] of int: L;

int: t = sum(duration);

int: p;


var int: makespan = max(t in TASK)(start[t] + duration[t]);

array[INDEX_SET_start_1] of var 0..t: start;

set of int: INDEX_SET_start_1;


include "cumulative.mzn";

constraint forall(i in PREC)(start[pre[i,1]] + duration[pre[i,1]] <= start[pre[i,2]]);

constraint forall(r in RESOURCE)(cumulative(start,duration,[res[r,t] | t in TASK],L[r]));



solve minimize makespan;




