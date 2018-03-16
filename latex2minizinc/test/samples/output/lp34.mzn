enum PERIODS;

array[INDEX_SET_STATES] of set of int: STATES;

array[int, int] of float: B;

array[int, int] of float: S;

PERIODS: NPeriods;

float: Kstrike;


array[INDEX_SET_C_1, INDEX_SET_C_2] of var float: C;

array[INDEX_SET_x_1, INDEX_SET_x_2] of var float: x;

array[INDEX_SET_y_1, INDEX_SET_y_2] of var float: y;

set of int: INDEX_SET_C_1;

set of int: INDEX_SET_C_2;

set of int: INDEX_SET_STATES;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;

set of int: INDEX_SET_y_1;

set of int: INDEX_SET_y_2;


constraint forall(p in PERIODS, s in STATES[p])(C[p,s] = x[p,s] * B[p,s] + y[p,s] * S[p,s]);

constraint forall(p in PERIODS, s in STATES[p] where p < NPeriods)(x[p,s] * B[p + 1,s] + y[p,s] * S[p + 1,s] >= C[p + 1,s]);

constraint forall(p in PERIODS, s in STATES[p] where p < NPeriods)(x[p,s] * B[p + 1,s + 1] + y[p,s] * S[p + 1,s + 1] >= C[p + 1,s + 1]);

constraint forall(p in PERIODS, s in STATES[p] where p < NPeriods)(x[p,s] * B[p + 1,s] + y[p,s] * S[p + 1,s] >= S[p + 1,s] - Kstrike);

constraint forall(p in PERIODS, s in STATES[p] where p < NPeriods)(x[p,s] * B[p + 1,s + 1] + y[p,s] * S[p + 1,s + 1] >= S[p + 1,s + 1] - Kstrike);

constraint forall(s in STATES[NPeriods])(C[NPeriods,s] >= max(0,S[NPeriods,s] - Kstrike));



solve minimize C[0,0];




