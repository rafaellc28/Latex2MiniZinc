enum JOBS;

array[int] of float: Rel;

array[int] of float: Dur;

array[int] of float: Due;

float: BigM;


array[int] of var float: start;

array[int] of var float: pastdue;

array[int, int] of var bool: y;


constraint forall(j in JOBS)(start[j] >= 0);

constraint forall(k in JOBS)(pastdue[k] >= 0);

constraint forall(k in JOBS)(start[k] >= Rel[k]);

constraint forall(k in JOBS)(start[k] + Dur[k] <= Due[k] + pastdue[k]);

constraint forall(j in JOBS, k in JOBS where j < k)(start[j] + Dur[j] <= start[k] + BigM * (1 - y[j,k]));

constraint forall(j in JOBS, k in JOBS where j < k)(start[k] + Dur[k] <= start[j] + BigM * y[j,k]);



var float: obj = sum(k in JOBS)(pastdue[k]);

solve minimize obj;




