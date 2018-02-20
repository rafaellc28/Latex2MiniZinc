enum JOBS;

array[int] of float: Rel;

array[int] of float: Dur;

array[int] of float: Due;

float: BigM;


array[INDEX_SET_start_1] of var float: start;

array[INDEX_SET_pastdue_1] of var float: pastdue;

array[INDEX_SET_y_1, INDEX_SET_y_2] of var bool: y;

set of int: INDEX_SET_pastdue_1;

set of int: INDEX_SET_start_1;

set of int: INDEX_SET_y_1;

set of int: INDEX_SET_y_2;


constraint forall(j in JOBS)(start[j] >= 0);

constraint forall(k in JOBS)(pastdue[k] >= 0);

constraint forall(k in JOBS)(start[k] >= Rel[k]);

constraint forall(k in JOBS)(start[k] + Dur[k] <= Due[k] + pastdue[k]);

constraint forall(j in JOBS, k in JOBS where j < k)(start[j] + Dur[j] <= start[k] + BigM * (1 - y[j,k]));

constraint forall(j in JOBS, k in JOBS where j < k)(start[k] + Dur[k] <= start[j] + BigM * y[j,k]);



solve minimize sum(k in JOBS)(pastdue[k]);




