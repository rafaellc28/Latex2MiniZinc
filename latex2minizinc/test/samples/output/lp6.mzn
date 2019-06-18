enum TASKS;

array[INDEX_SET_ARCS, 1..2] of TASKS: ARCS;

array[TASKS] of float: Dur;


array[TASKS] of var float: Tef;

var float: Tf;

array[TASKS] of var float: Tlf;

array[TASKS] of var float: Tes;

array[TASKS] of var float: Tls;

array[TASKS] of var float: Tsl;

set of int: INDEX_SET_ARCS;


constraint forall(j in TASKS)(Tef[j] >= 0);

constraint Tf >= 0;

constraint forall(j in TASKS)(Tlf[j] >= 0);

constraint forall(j in TASKS)(Tes[j] >= 0);

constraint forall(j in TASKS)(Tls[j] >= 0);

constraint forall(j in TASKS)(Tsl[j] >= 0);

constraint forall(j in TASKS)(Tef[j] <= Tf);

constraint forall(j in TASKS)(Tlf[j] <= Tf);

constraint forall(j in TASKS)(Tef[j] = Tes[j] + Dur[j]);

constraint forall(j in TASKS)(Tlf[j] = Tls[j] + Dur[j]);

constraint forall(j in TASKS)(Tsl[j] = Tls[j] - Tes[j]);

constraint forall(i in INDEX_SET_ARCS)(Tef[ARCS[i,1]] <= Tes[ARCS[i,2]]);

constraint forall(j in INDEX_SET_ARCS)(Tlf[ARCS[j,1]] <= Tls[ARCS[j,2]]);



solve minimize card(TASKS) * Tf - sum(j in TASKS)(Tsl[j]);




