enum SENSORS;

enum STREAMS;

enum UNITS;

float: BigM;

array[int, int] of float: A;

array[int] of float: Y;

array[int] of STREAMS: S;

array[int] of float: Emax;


array[int] of var bool: gerr;

array[int] of var float: epos;

array[int] of var float: eneg;

array[int] of var float: x;


constraint forall(k in SENSORS)(epos[k] >= 0);

constraint forall(k in SENSORS)(eneg[k] >= 0);

constraint forall(j in STREAMS)(x[j] >= 0);

constraint forall(i in UNITS)(sum(j in STREAMS)(A[i,j] * x[j]) = 0);

constraint forall(k in SENSORS)(Y[k] = x[S[k]] + epos[k] - eneg[k]);

constraint forall(k in SENSORS)(epos[k] <= Emax[k] + BigM * gerr[k]);

constraint forall(k in SENSORS)(eneg[k] <= Emax[k] + BigM * gerr[k]);

constraint forall(j in STREAMS)(x[j] >= 0);



var float: obj = sum(k in SENSORS)((epos[k] + eneg[k] + BigM * gerr[k]));

solve minimize obj;




