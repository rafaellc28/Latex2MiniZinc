enum PERIODS;

array[INDEX_SET_STATES] of set of int: STATES;

array[int, int] of float: B;

array[int, int] of float: S;

PERIODS: NPeriods;

float: Kstrike;


array[INDEX_SET_P_1, INDEX_SET_P_2] of var float: P;

array[INDEX_SET_x_1, INDEX_SET_x_2] of var float: x;

array[INDEX_SET_y_1, INDEX_SET_y_2] of var float: y;

set of int: INDEX_SET_P_1 = PERIODS;

set of int: INDEX_SET_P_2;

set of int: INDEX_SET_STATES;

set of int: INDEX_SET_x_1 = PERIODS;

set of int: INDEX_SET_x_2;

set of int: INDEX_SET_y_1 = PERIODS;

set of int: INDEX_SET_y_2;


constraint forall(p in PERIODS, s in STATES[p])(P[p,s] = x[p,s] * B[p,s] + y[p,s] * S[p,s]);

constraint forall(p in PERIODS, s in STATES[p] where p < NPeriods)(x[p,s] * B[p + 1,s] + y[p,s] * S[p + 1,s] >= P[p + 1,s]);

constraint forall(p in PERIODS, s in STATES[p] where p < NPeriods)(x[p,s] * B[p + 1,s + 1] + y[p,s] * S[p + 1,s + 1] >= P[p + 1,s + 1]);

constraint forall(s in STATES[NPeriods])(P[NPeriods,s] >= max(0,Kstrike - S[NPeriods,s]));



solve minimize P[0,0];




