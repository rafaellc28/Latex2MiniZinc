set of int: I = 1..Lsup;

int: Lsup = N / 2 - 1;

int: N;


array[I] of var float: x = array1d(I, [0.5 | i in I]);

array[I] of var float: y = array1d(I, [i / Lsup | i in I]);


constraint assert(N > 1, "Assertion N > 1 failed!");

constraint forall(i in ceil(Lsup / 2)..Lsup, j in max(1,Lsup - i)..min(Lsup + 1 - i,i))(pow((x[i] + x[j]),2) + pow((y[i] - y[j]),2) = 1);

constraint pow(x[Lsup],2) + pow(y[Lsup],2) = 1;

constraint forall(i in 2..Lsup)(y[i] >= y[i - 1]);



solve maximize sum(i in 2..floor(Lsup - 1))(y[i] * (x[i - 1] - x[i + 1]) + x[Lsup] + y[Lsup] * x[Lsup - 1] - x[2] * y[1]);




