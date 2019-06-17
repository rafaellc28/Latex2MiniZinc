enum SENSORS;

enum STREAMS;

enum UNITS;

float: BigM;

array[UNITS, STREAMS] of float: A;

array[SENSORS] of float: Y;

array[SENSORS] of STREAMS: S;

array[SENSORS] of float: Emax;


array[SENSORS] of var bool: gerr;

array[SENSORS] of var float: epos;

array[SENSORS] of var float: eneg;

array[STREAMS] of var float: x;


constraint forall(k in SENSORS)(epos[k] >= 0);

constraint forall(k in SENSORS)(eneg[k] >= 0);

constraint forall(j in STREAMS)(x[j] >= 0);

constraint forall(i in UNITS)(sum(j in STREAMS)(A[i,j] * x[j]) = 0);

constraint forall(k in SENSORS)(Y[k] = x[S[k]] + epos[k] - eneg[k]);

constraint forall(k in SENSORS)(epos[k] <= Emax[k] + BigM * gerr[k]);

constraint forall(k in SENSORS)(eneg[k] <= Emax[k] + BigM * gerr[k]);

constraint forall(j in STREAMS)(x[j] >= 0);



solve minimize sum(k in SENSORS)((epos[k] + eneg[k] + BigM * gerr[k]));




