set of int: PERIODS = 0..nPeriods;

array[INDEX_SET_STATES_1] of set of int: STATES = array1d(INDEX_SET_STATES_1, [0..p | p in PERIODS]);

array[INDEX_SET_B_1, INDEX_SET_B_2] of float: B = array2d(INDEX_SET_B_1, INDEX_SET_B_2, [B0 * pow((1 + rf * Tf / nPeriods),p) | p in PERIODS, s in STATES[p]]);

array[INDEX_SET_S_1, INDEX_SET_S_2] of float: S = array2d(INDEX_SET_S_1, INDEX_SET_S_2, [S0 * (pow(d,p - to_enum(PERIODS,s))) * (pow(u,to_enum(PERIODS,s))) | p in PERIODS, s in STATES[p]]);

int: nPeriods = 10;

float: Kstrike = 110;

float: S0 = 100;

float: r = 0.06;

float: sigma = 0.3;

float: B0 = 1;

float: rf = 0.03;

float: Tf = 1;

float: u = exp(sigma * sqrt(Tf / nPeriods));

float: d = 1 / u;

float: pr = (exp(r * Tf / nPeriods) - d) / (u - d);


array[INDEX_SET_C_1, INDEX_SET_C_2] of var float: C;

array[INDEX_SET_x_1, INDEX_SET_x_2] of var float: x;

array[INDEX_SET_y_1, INDEX_SET_y_2] of var float: y;

set of int: INDEX_SET_B_1;

set of int: INDEX_SET_B_2;

set of int: INDEX_SET_C_1;

set of int: INDEX_SET_C_2;

set of int: INDEX_SET_STATES_1;

set of int: INDEX_SET_S_1;

set of int: INDEX_SET_S_2;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;

set of int: INDEX_SET_y_1;

set of int: INDEX_SET_y_2;


constraint forall(p in PERIODS, s in STATES[p])(C[p,to_enum(PERIODS,s)] = x[p,to_enum(PERIODS,s)] * B[p,to_enum(PERIODS,s)] + y[p,to_enum(PERIODS,s)] * S[p,to_enum(PERIODS,s)]);

constraint forall(p in PERIODS, s in STATES[p] where p < nPeriods)(x[p,to_enum(PERIODS,s)] * B[p + 1,to_enum(PERIODS,s)] + y[p,to_enum(PERIODS,s)] * S[p + 1,to_enum(PERIODS,s)] >= C[p + 1,to_enum(PERIODS,s)]);

constraint forall(p in PERIODS, s in STATES[p] where p < nPeriods)(x[p,to_enum(PERIODS,s)] * B[p + 1,to_enum(PERIODS,s) + 1] + y[p,to_enum(PERIODS,s)] * S[p + 1,to_enum(PERIODS,s) + 1] >= C[p + 1,to_enum(PERIODS,s) + 1]);

constraint forall(s in STATES[nPeriods])(C[nPeriods,to_enum(PERIODS,s)] >= max(0,S[nPeriods,to_enum(PERIODS,s)] - Kstrike));



var float: obj = C[0,0];

solve minimize obj;




