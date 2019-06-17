set of int: MACHINES = 1..n;

set of int: JOBS = 1..n;

array[MACHINES] of int: cap;

int: n;


array[JOBS, MACHINES] of var bool: Assign;


constraint forall(k in MACHINES)(assert(cap[k] >= 0, "Assertion cap[\(k)] >= 0 failed!"));

constraint assert(n > 0, "Assertion n > 0 failed!");

constraint forall(j in JOBS)(sum(k in MACHINES)(Assign[j,k]) = 1);

constraint forall(k in MACHINES)(sum(j in JOBS)(Assign[j,k]) <= cap[k]);

solve satisfy;


