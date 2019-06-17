enum SENSORS;

enum STREAMS;

enum UNITS;

float: bigM = 100;

array[UNITS, STREAMS] of float: A;

array[SENSORS] of float: y;

array[SENSORS] of STREAMS: s;

array[SENSORS] of float: emax;


array[STREAMS] of var float: x;

array[STREAMS] of var float: epos;

array[STREAMS] of var float: eneg;

array[STREAMS] of var bool: gerr;


constraint forall(k in SENSORS)(assert(y[k] >= 0, "Assertion y[\(k)] >= 0 failed!"));

constraint forall(k in SENSORS)(assert(s[k] > 0, "Assertion s[\(k)] > 0 failed!"));

constraint forall(k in SENSORS)(assert(emax[k] >= 0, "Assertion emax[\(k)] >= 0 failed!"));

constraint forall(k in STREAMS)(x[k] >= 0);

constraint forall(k in STREAMS)(epos[k] >= 0);

constraint forall(k in STREAMS)(eneg[k] >= 0);

constraint forall(i in UNITS)(sum(j in STREAMS)(A[i,j] * x[j]) = 0);

constraint forall(k in SENSORS)(y[k] = x[s[k]] + epos[to_enum(STREAMS,k)] - eneg[to_enum(STREAMS,k)]);

constraint forall(k in SENSORS)(epos[to_enum(STREAMS,k)] <= emax[k] + bigM * gerr[to_enum(STREAMS,k)]);

constraint forall(k in SENSORS)(eneg[to_enum(STREAMS,k)] <= emax[k] + bigM * gerr[to_enum(STREAMS,k)]);



solve minimize sum(k in SENSORS)((epos[to_enum(STREAMS,k)] + eneg[to_enum(STREAMS,k)] + bigM * gerr[to_enum(STREAMS,k)]));




