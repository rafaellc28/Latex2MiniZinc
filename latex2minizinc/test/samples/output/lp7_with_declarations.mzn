enum JOBS;

array[JOBS] of float: dur;

array[JOBS] of float: due;

array[JOBS] of float: rel;

float: bigM = (max(k in JOBS)(rel[k])) + sum(k in JOBS)(dur[k]);


array[JOBS] of var float: start;

array[JOBS] of var float: pastdue;

array[JOBS, JOBS] of var bool: y;


constraint forall(k in JOBS)(start[k] >= 0);

constraint forall(k in JOBS)(pastdue[k] >= 0);

constraint forall(k in JOBS)(start[k] >= rel[k]);

constraint forall(k in JOBS)(start[k] + dur[k] <= due[k] + pastdue[k]);

constraint forall(j in JOBS, k in JOBS where j < k)(start[j] + dur[j] <= start[k] + bigM * (1 - y[j,k]));

constraint forall(j in JOBS, k in JOBS where j < k)(start[k] + dur[k] <= start[j] + bigM * y[j,k]);



var float: obj = sum(k in JOBS)(pastdue[k]);

solve minimize obj;




