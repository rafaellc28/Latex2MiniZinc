set of int: PERIODS = 0..nPeriods;

array[PERIODS] of set of int: STATES = array1d(PERIODS, [0..p | p in PERIODS]);

array[PERIODS, INDEX_SET_B_2] of float: B = array2d(PERIODS, INDEX_SET_B_2, [B0 * pow((1 + rf * Tf / nPeriods),p) | p in PERIODS, s in STATES[p]]);

array[PERIODS, INDEX_SET_S_2] of float: S = array2d(PERIODS, INDEX_SET_S_2, [S0 * (pow(d,p - s)) * (pow(u,s)) | p in PERIODS, s in STATES[p]]);

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


array[PERIODS, INDEX_SET_C_2] of var float: C;

array[PERIODS, INDEX_SET_x_2] of var float: x;

array[PERIODS, INDEX_SET_y_2] of var float: y;

set of int: INDEX_SET_B_2;

set of int: INDEX_SET_C_2;

set of int: INDEX_SET_S_2;

set of int: INDEX_SET_x_2;

set of int: INDEX_SET_y_2;


constraint forall(p in PERIODS, s in STATES[p])(C[p,s] = x[p,s] * B[p,s] + y[p,s] * S[p,s]);

constraint forall(p in PERIODS, s in STATES[p] where p < nPeriods)(x[p,s] * B[p + 1,s] + y[p,s] * S[p + 1,s] >= C[p + 1,s]);

constraint forall(p in PERIODS, s in STATES[p] where p < nPeriods)(x[p,s] * B[p + 1,s + 1] + y[p,s] * S[p + 1,s + 1] >= C[p + 1,s + 1]);

constraint forall(s in STATES[nPeriods])(C[nPeriods,s] >= max(0,S[nPeriods,s] - Kstrike));



solve minimize C[0,0];




