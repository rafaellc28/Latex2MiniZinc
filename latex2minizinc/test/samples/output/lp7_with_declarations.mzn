enum JOBS;

array[int] of float: rel;

array[int] of float: dur;

array[int] of float: due;

float: bigM = (max(k in JOBS)(rel[k])) + sum(k in JOBS)(dur[k]);


array[INDEX_SET_start_1] of var float: start;

array[INDEX_SET_pastdue_1] of var float: pastdue;

array[INDEX_SET_y_1, INDEX_SET_y_2] of var bool: y;

set of int: INDEX_SET_pastdue_1 = JOBS;

set of int: INDEX_SET_start_1 = JOBS;

set of int: INDEX_SET_y_1 = JOBS;

set of int: INDEX_SET_y_2 = JOBS;


constraint forall(k in INDEX_SET_start_1)(start[k] >= 0);

constraint forall(k in INDEX_SET_pastdue_1)(pastdue[k] >= 0);

constraint forall(k in JOBS)(start[k] >= rel[k]);

constraint forall(k in JOBS)(start[k] + dur[k] <= due[k] + pastdue[k]);

constraint forall(j,k in JOBS where j < k)(start[j] + dur[j] <= start[k] + bigM * (1 - y[j,k]));

constraint forall(j,k in JOBS where j < k)(start[k] + dur[k] <= start[j] + bigM * y[j,k]);



solve minimize sum(k in JOBS)(pastdue[k]);




