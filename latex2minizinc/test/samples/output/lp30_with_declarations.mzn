enum SENSORS;

enum STREAMS;

enum UNITS;

float: bigM = 100;

array[int, int] of float: A;

array[int] of float: y;

array[int] of STREAMS: s;

array[int] of float: emax;


array[INDEX_SET_x_1] of var float: x;

array[INDEX_SET_epos_1] of var float: epos;

array[INDEX_SET_eneg_1] of var float: eneg;

array[INDEX_SET_gerr_1] of var bool: gerr;

set of int: INDEX_SET_eneg_1 = STREAMS;

set of int: INDEX_SET_epos_1 = STREAMS;

set of int: INDEX_SET_gerr_1 = STREAMS;

set of int: INDEX_SET_x_1 = STREAMS;


constraint forall(k in SENSORS)(assert(y[k] >= 0, "Assertion y[\(k)] >= 0 failed!"));

constraint forall(k in SENSORS)(assert(s[k] > 0, "Assertion s[\(k)] > 0 failed!"));

constraint forall(k in SENSORS)(assert(emax[k] >= 0, "Assertion emax[\(k)] >= 0 failed!"));

constraint forall(k in INDEX_SET_x_1)(x[k] >= 0);

constraint forall(k in INDEX_SET_epos_1)(epos[k] >= 0);

constraint forall(k in INDEX_SET_eneg_1)(eneg[k] >= 0);

constraint forall(i in UNITS)(sum(j in STREAMS)(A[i,j] * x[j]) = 0);

constraint forall(k in SENSORS)(y[k] = x[s[k]] + epos[k] - eneg[k]);

constraint forall(k in SENSORS)(epos[k] <= emax[k] + bigM * gerr[k]);

constraint forall(k in SENSORS)(eneg[k] <= emax[k] + bigM * gerr[k]);



solve minimize sum(k in SENSORS)((epos[k] + eneg[k] + bigM * gerr[k]));




