set of int: PREC = 1..p;

set of TASK: LIU;

enum TASK;

array[PREC, 1..2] of TASK: pre;

array[TASK] of int: duration;

int: t = sum(duration);

int: p;


array[TASK] of var 0..t: start;

var 0..t: makespan = max(t in TASK)(start[t] + duration[t]);


constraint forall(i in PREC)(start[pre[i,1]] + duration[pre[i,1]] <= start[pre[i,2]]);

predicate nonoverlap(var int: s1, var int: d1, var int: s2, var int: d2) =
	s1 + d1 <= s2 \/ s2 + d2 <= s1;

constraint forall(t1,t2 in LIU where t1 < t2)(nonoverlap(start[t1],duration[t1],start[t2],duration[t2]));



solve minimize makespan;




