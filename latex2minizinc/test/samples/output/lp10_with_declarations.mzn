enum TASKS = {Kitchen,Bathroom,Commons,Trash};

set of int: VOLS = 1..7;

set of int: WEEKS = 1..T;

array[INDEX_SET_PAIRS, 1..2] of int: PAIRS = array2d(INDEX_SET_PAIRS, 1..2, [if idx2 = 1 then u else v endif | u in VOLS, v in VOLS, idx2 in 1..2 where u < v]);

int: T = 7;


array[VOLS, TASKS, WEEKS] of var bool: x;

array[INDEX_SET_p_1, INDEX_SET_p_2, TASKS, WEEKS] of var bool: p;

var int: z;

set of int: INDEX_SET_PAIRS;

set of int: INDEX_SET_p_1 = PAIRS;

set of int: INDEX_SET_p_2 = TASKS;


constraint forall(v in VOLS, w in WEEKS)(sum(t in TASKS)(x[v,t,w]) = 1);

constraint forall(w in WEEKS)(sum(v in VOLS)(x[v,Trash,w]) = 1);

constraint forall(t in TASKS, w in WEEKS where t != Trash)(sum(v in VOLS)(x[v,t,w]) = 2);

constraint forall(t in TASKS, v in VOLS where t != Trash)(sum(w in WEEKS)(x[v,t,w]) >= 2);

constraint forall(v in VOLS)(sum(w in WEEKS)(x[v,Trash,w]) <= z);

constraint forall(t in TASKS, w in WEEKS, u in INDEX_SET_PAIRS)(p[PAIRS[u,1],PAIRS[u,2],t,w] <= x[PAIRS[u,1],t,w]);

constraint forall(t in TASKS, w in WEEKS, u in INDEX_SET_PAIRS)(p[PAIRS[u,1],PAIRS[u,2],t,w] <= x[PAIRS[u,2],t,w]);

constraint forall(t in TASKS, w in WEEKS, u in INDEX_SET_PAIRS)(p[PAIRS[u,1],PAIRS[u,2],t,w] >= x[PAIRS[u,1],t,w] + x[PAIRS[u,2],t,w] - 1);

constraint forall(u in INDEX_SET_PAIRS)(sum(t in TASKS, w in WEEKS)(p[PAIRS[u,1],PAIRS[u,2],t,w]) >= 1);



solve minimize z;




