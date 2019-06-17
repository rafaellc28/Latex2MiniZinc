enum JOBS;

array[JOBS] of float: Rel;

array[JOBS] of float: Dur;

array[JOBS] of float: Due;

float: BigM;


array[JOBS] of var float: start;

array[JOBS] of var float: pastdue;

array[JOBS, JOBS] of var bool: y;


constraint forall(j in JOBS)(start[j] >= 0);

constraint forall(k in JOBS)(pastdue[k] >= 0);

constraint forall(k in JOBS)(start[k] >= Rel[k]);

constraint forall(k in JOBS)(start[k] + Dur[k] <= Due[k] + pastdue[k]);

constraint forall(j,k in JOBS where j < k)(start[j] + Dur[j] <= start[k] + BigM * (1 - y[j,k]));

constraint forall(j,k in JOBS where j < k)(start[k] + Dur[k] <= start[j] + BigM * y[j,k]);



solve minimize sum(k in JOBS)(pastdue[k]);




