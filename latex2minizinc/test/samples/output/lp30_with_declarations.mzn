enum SENSORS;

enum STREAMS;

enum UNITS;

float: bigM = 100;

array[int, int] of float: A;

array[int] of float: y;

array[int] of STREAMS: s;

array[int] of float: emax;


array[int] of var float: x;

array[int] of var float: epos;

array[int] of var float: eneg;

array[int] of var bool: gerr;


constraint forall(k in STREAMS)(x[k] >= 0);

constraint forall(k in STREAMS)(epos[k] >= 0);

constraint forall(k in STREAMS)(eneg[k] >= 0);

constraint forall(i in UNITS)(sum(j in STREAMS)(A[i,j] * x[j]) = 0);

constraint forall(k in SENSORS)(y[k] = x[s[k]] + epos[k] - eneg[k]);

constraint forall(k in SENSORS)(epos[k] <= emax[k] + bigM * gerr[k]);

constraint forall(k in SENSORS)(eneg[k] <= emax[k] + bigM * gerr[k]);



var float: obj = sum(k in SENSORS)((epos[k] + eneg[k] + bigM * gerr[k]));

solve minimize obj;




