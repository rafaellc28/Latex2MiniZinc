enum SENSORS;

enum STREAMS;

enum UNITS;

float: BigM;

array[int, int] of float: A;

array[int] of float: Y;

array[int] of STREAMS: S;

array[int] of float: Emax;


array[INDEX_SET_gerr_1] of var bool: gerr;

array[INDEX_SET_epos_1] of var float: epos;

array[INDEX_SET_eneg_1] of var float: eneg;

array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_eneg_1;

set of int: INDEX_SET_epos_1;

set of int: INDEX_SET_gerr_1;

set of int: INDEX_SET_x_1;


constraint forall(k in SENSORS)(epos[k] >= 0);

constraint forall(k in SENSORS)(eneg[k] >= 0);

constraint forall(j in STREAMS)(x[j] >= 0);

constraint forall(i in UNITS)(sum(j in STREAMS)(A[i,j] * x[j]) = 0);

constraint forall(k in SENSORS)(Y[k] = x[S[k]] + epos[k] - eneg[k]);

constraint forall(k in SENSORS)(epos[k] <= Emax[k] + BigM * gerr[k]);

constraint forall(k in SENSORS)(eneg[k] <= Emax[k] + BigM * gerr[k]);

constraint forall(j in STREAMS)(x[j] >= 0);



solve minimize sum(k in SENSORS)((epos[k] + eneg[k] + BigM * gerr[k]));




