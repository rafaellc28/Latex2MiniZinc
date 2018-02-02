enum JOBS;

float: n;


array[INDEX_SET_MachineForJob_1] of var int: MachineForJob;

set of int: INDEX_SET_MachineForJob_1;


constraint forall(j2 in JOBS)(MachineForJob[j2] >= 1);

constraint forall(j2 in JOBS)(MachineForJob[j2] <= n);

constraint forall(j1 in JOBS, j2 in JOBS where j1 < j2)(MachineForJob[j1] != MachineForJob[j2]);

solve satisfy;


