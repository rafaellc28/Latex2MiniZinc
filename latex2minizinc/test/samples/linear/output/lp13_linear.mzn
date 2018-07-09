set of int: I = 1..N;

int: N;

float: pi = 4 * atan(1);


array[INDEX_SET_rho_1] of var float: rho = array1d(INDEX_SET_rho_1, [4 * i * (N + 1 - i) / pow((N + 1),2) | i in I]);

array[INDEX_SET_the_1] of var float: the = array1d(INDEX_SET_the_1, [pi * i / N | i in I]);

set of int: INDEX_SET_rho_1 = I;

set of int: INDEX_SET_the_1 = I;


constraint assert(N > 0, "Assertion N > 0 failed!");

constraint forall(i in I, j in floor(i + 1)..N)(pow(rho[i],2) + pow(rho[j],2) - 2 * rho[i] * rho[j] * cos(the[j] - the[i]) <= 1);

constraint forall(i in 2..N)(the[i] >= the[i - 1]);

constraint the[N] = pi;

constraint rho[N] = 0;



solve maximize 0.5 * sum(i in 2..N)(rho[i] * rho[i - 1] * sin(the[i] - the[i - 1]));




