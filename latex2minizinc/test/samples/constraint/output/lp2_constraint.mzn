array[1..nMach, 1..nJobs] of float: duration;

int: nMach;

int: nJobs;

int: endTime;


var int: Makespan;

array[1..nMach, 1..nJobs] of var int: Start;


constraint assert(nMach > 0, "Assertion nMach > 0 failed!");

constraint assert(nJobs > 0, "Assertion nJobs > 0 failed!");

constraint assert(endTime > 0, "Assertion endTime > 0 failed!");

constraint Makespan >= 0;

constraint Makespan <= endTime;

constraint forall(i in 1..nMach, j in 1..nJobs)(Start[i,j] >= 0);

constraint forall(i in 1..nMach, j in 1..nJobs)(Start[i,j] <= endTime);

constraint forall(m in 1..nMach, j1 in 1..nJobs, j2 in floor(j1 + 1)..nJobs)(Start[m,j1] + duration[m,j1] <= Start[m,j2] \/ Start[m,j2] + duration[m,j2] <= Start[m,j1]);

constraint forall(m1 in 1..nMach, m2 in floor(m1 + 1)..nMach, j in 1..nJobs)(Start[m1,j] + duration[m1,j] <= Start[m2,j] \/ Start[m2,j] + duration[m2,j] <= Start[m1,j]);

constraint forall(m in 1..nMach, j in 1..nJobs)(Start[m,j] + duration[m,j] <= Makespan);



solve minimize Makespan;




