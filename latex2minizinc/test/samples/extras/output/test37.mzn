set of int: MACHINES = 1..n;

set of int: JOBS = 1..n;

array[int] of int: cap;

int: n;


array[INDEX_SET_Assign_1, INDEX_SET_Assign_2] of var bool: Assign;

set of int: INDEX_SET_Assign_1;

set of int: INDEX_SET_Assign_2;


constraint forall(j in JOBS)(sum(k in MACHINES)(Assign[j,k]) = 1);

constraint forall(k in MACHINES)(sum(j in JOBS)(Assign[j,k]) <= cap[k]);

solve satisfy;


