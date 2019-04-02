set of int: PREC = 1..p;

enum TASK;

array[int, int] of TASK: pre;

array[int] of int: duration;

set of TASK: LIU;

set of TASK: ZHANG;

set of TASK: GUAN;

int: t = sum(duration);

int: p;


array[INDEX_SET_start_1] of var 0..t: start;

var 0..t: makespan = max(t in TASK)(start[t] + duration[t]);

set of int: INDEX_SET_start_1 = TASK;


constraint forall(i in PREC)(start[pre[i,1]] + duration[pre[i,1]] <= start[pre[i,2]]);

predicate nonoverlap(var int: s1, var int: d1, var int: s2, var int: d2) =
	s1 + d1 <= s2 \/ s2 + d2 <= s1;

predicate exclusive(var set of TASK: tasks) =
	forall(t1,t2 in tasks where t1 < t2)(nonoverlap(start[t1],duration[t1],start[t2],duration[t2]));

constraint exclusive(LIU);

constraint exclusive(ZHANG);

constraint exclusive(GUAN);



solve minimize makespan;




