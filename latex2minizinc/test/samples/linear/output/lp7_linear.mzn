enum ACT;

enum MAT;

array[int] of float: revenue;

array[int, int] of float: io;

array[int] of float: act_min;

array[int] of float: act_max;


array[INDEX_SET_Run_1] of var float: Run;

set of int: INDEX_SET_Run_1;


constraint forall(j in ACT)(Run[j] <= act_max[j] /\ Run[j] >= act_min[j]);

constraint forall(i in MAT)(sum(j in ACT)(io[i,j] * Run[j]) = 0);



solve maximize sum(j in ACT)(revenue[j] * Run[j]);




