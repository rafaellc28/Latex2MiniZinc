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


constraint forall(p in PERIODS, s in STATES[p])(C[p,to_enum(PERIODS,s)] = x[p,to_enum(PERIODS,s)] * B[p,to_enum(PERIODS,s)] + y[p,to_enum(PERIODS,s)] * S[p,to_enum(PERIODS,s)]);

constraint forall(p in PERIODS, s in STATES[p] where p < NPeriods)(x[p,to_enum(PERIODS,s)] * B[p + 1,to_enum(PERIODS,s)] + y[p,to_enum(PERIODS,s)] * S[p + 1,to_enum(PERIODS,s)] >= C[p + 1,to_enum(PERIODS,s)]);

constraint forall(p in PERIODS, s in STATES[p] where p < NPeriods)(x[p,to_enum(PERIODS,s)] * B[p + 1,to_enum(PERIODS,s) + 1] + y[p,to_enum(PERIODS,s)] * S[p + 1,to_enum(PERIODS,s) + 1] >= C[p + 1,to_enum(PERIODS,s) + 1]);

constraint forall(s in STATES[NPeriods])(C[NPeriods,to_enum(PERIODS,s)] >= max(0,S[NPeriods,to_enum(PERIODS,s)] - Kstrike));



var float: obj = C[0,0];

solve minimize obj;




