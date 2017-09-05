enum TASKS;

array[INDEX_SET_ARCS, 1..2] of TASKS: ARCS;

array[int] of float: Dur;

set of int: INDEX_SET_ARCS;


array[int] of var float: Tef;

var float: Tf;

array[int] of var float: Tlf;

array[int] of var float: Tes;

array[int] of var float: Tls;

array[int] of var float: Tsl;


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



var float: obj = card(TASKS) * Tf - sum(j in TASKS)(Tsl[j]);

solve minimize obj;




