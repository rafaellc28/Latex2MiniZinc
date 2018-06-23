set of int: I = 1..Lsup;

int: Lsup = N / 2 - 1;

int: N;


array[INDEX_SET_x_1] of var float: x = array1d(INDEX_SET_x_1, [0.5 | i in I]);

array[INDEX_SET_y_1] of var float: y = array1d(INDEX_SET_y_1, [i / Lsup | i in I]);

set of int: INDEX_SET_x_1 = I;

set of int: INDEX_SET_y_1 = I;


constraint forall(i in ceil(Lsup / 2)..Lsup, j in max(1,Lsup - i)..min(Lsup + 1 - i,i))(pow((x[i] + x[j]),2) + pow((y[i] - y[j]),2) = 1);

constraint pow(x[Lsup],2) + pow(y[Lsup],2) = 1;

constraint forall(i in 2..Lsup)(y[i] >= y[i - 1]);



solve maximize sum(i in 2..floor(Lsup - 1))(y[i] * (x[i - 1] - x[i + 1]) + x[Lsup] + y[Lsup] * x[Lsup - 1] - x[2] * y[1]);




