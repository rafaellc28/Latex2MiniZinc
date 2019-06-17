enum JOBS;

array[JOBS] of float: rel;

array[JOBS] of float: dur;

array[JOBS] of float: due;

float: bigM = (max(k in JOBS)(rel[k])) + sum(k in JOBS)(dur[k]);


array[JOBS] of var float: start;

array[JOBS] of var float: pastdue;

array[JOBS, JOBS] of var bool: y;


constraint forall(k in JOBS)(start[k] >= 0);

constraint forall(k in JOBS)(pastdue[k] >= 0);

constraint forall(k in JOBS)(start[k] >= rel[k]);

constraint forall(k in JOBS)(start[k] + dur[k] <= due[k] + pastdue[k]);

constraint forall(j,k in JOBS where j < k)(start[j] + dur[j] <= start[k] + bigM * (1 - y[j,k]));

constraint forall(j,k in JOBS where j < k)(start[k] + dur[k] <= start[j] + bigM * y[j,k]);



solve minimize sum(k in JOBS)(pastdue[k]);




