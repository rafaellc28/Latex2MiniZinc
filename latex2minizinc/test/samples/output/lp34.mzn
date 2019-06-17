enum PERIODS;

array[INDEX_SET_STATES] of set of int: STATES;

array[PERIODS, int] of float: B;

array[PERIODS, int] of float: S;

PERIODS: NPeriods;

float: Kstrike;


array[PERIODS, INDEX_SET_C_2] of var float: C;

array[PERIODS, INDEX_SET_x_2] of var float: x;

array[PERIODS, INDEX_SET_y_2] of var float: y;

set of int: INDEX_SET_C_2;

set of int: INDEX_SET_STATES;

set of int: INDEX_SET_x_2;

set of int: INDEX_SET_y_2;


constraint forall(p in PERIODS, s in STATES[p])(C[p,s] = x[p,s] * B[p,s] + y[p,s] * S[p,s]);

constraint forall(p in PERIODS, s in STATES[p] where p < NPeriods)(x[p,s] * B[to_enum(PERIODS,p + 1),s] + y[p,s] * S[to_enum(PERIODS,p + 1),s] >= C[to_enum(PERIODS,p + 1),s]);

constraint forall(p in PERIODS, s in STATES[p] where p < NPeriods)(x[p,s] * B[to_enum(PERIODS,p + 1),s + 1] + y[p,s] * S[to_enum(PERIODS,p + 1),s + 1] >= C[to_enum(PERIODS,p + 1),s + 1]);

constraint forall(p in PERIODS, s in STATES[p] where p < NPeriods)(x[p,s] * B[to_enum(PERIODS,p + 1),s] + y[p,s] * S[to_enum(PERIODS,p + 1),s] >= S[to_enum(PERIODS,p + 1),s] - Kstrike);

constraint forall(p in PERIODS, s in STATES[p] where p < NPeriods)(x[p,s] * B[to_enum(PERIODS,p + 1),s + 1] + y[p,s] * S[to_enum(PERIODS,p + 1),s + 1] >= S[to_enum(PERIODS,p + 1),s + 1] - Kstrike);

constraint forall(s in STATES[NPeriods])(C[NPeriods,s] >= max(0,S[NPeriods,s] - Kstrike));



solve minimize C[to_enum(PERIODS,0),0];




