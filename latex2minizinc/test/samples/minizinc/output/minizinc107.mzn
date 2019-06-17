set of int: PREC = 1..p;

enum TASK;

array[PREC, 1..2] of TASK: pre;

array[TASK] of int: duration;

set of TASK: LIU;

set of TASK: ZHANG;

set of TASK: GUAN;

int: t = sum(duration);

int: p;


array[TASK] of var 0..t: start;

var 0..t: makespan = max(t in TASK)(start[t] + duration[t]);


include "disjunctive.mzn";

constraint forall(i in PREC)(start[pre[i,1]] + duration[pre[i,1]] <= start[pre[i,2]]);

predicate exclusive(set of TASK: tasks) =
	let {array[int] of var int: sa = [start[t] | t in tasks]; array[int] of int: dd = [duration[t] | t in tasks]} in
	disjunctive(sa,dd);

constraint exclusive(LIU);

constraint exclusive(ZHANG);

constraint exclusive(GUAN);



solve minimize makespan;




