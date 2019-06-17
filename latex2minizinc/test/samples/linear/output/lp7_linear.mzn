enum ACT;

enum MAT;

array[ACT] of float: revenue;

array[MAT, ACT] of float: io;

array[ACT] of float: act_min;

array[ACT] of float: act_max;


array[ACT] of var float: Run;


constraint forall(j in ACT)(assert(act_min[j] >= 0, "Assertion act_min[\(j)] >= 0 failed!"));

constraint forall(j in ACT)(assert(act_max[j] >= act_min[j], "Assertion act_max[\(j)] >= act_min[\(j)] failed!"));

constraint forall(j in ACT)(Run[j] <= act_max[j] /\ Run[j] >= act_min[j]);

constraint forall(i in MAT)(sum(j in ACT)(io[i,j] * Run[j]) = 0);



solve maximize sum(j in ACT)(revenue[j] * Run[j]);




