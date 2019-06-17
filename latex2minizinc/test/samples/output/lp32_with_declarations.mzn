enum EXPENSES = {TuitionA,TuitionB,TuitionC};

set of int: N = 0..Nper;

array[N] of float: salary = array1d(N, [(150000 * pow((1 + rf),n)) * (0.4 + 0.1 * t[n]) / (1 + 0.1 * t[n]) | n in N]);

float: Rf = 0.03;

float: dT = T / Nper;

float: Wi = 0;

float: Ri = 0.05;

int: Nper = floor(1 * T);

float: T = 40;

array[N] of float: t = array1d(N, [n * dT | n in N]);

float: ri = Ri * dT;

float: rf = Rf * dT;


array[N] of var float: w;

array[N] of var float: u;

array[N, EXPENSES] of var float: x;

var float: fSave;


constraint forall(n in N)(w[n] >= 0);

constraint forall(n in N)(u[n] >= 0);

constraint forall(n in N, e in EXPENSES)(x[n,e] >= 0);

constraint w[Nper] = 8 * salary[Nper];

constraint forall(n in floor(18 / dT)..floor(21 / dT))(x[n,TuitionA] = 40000 * pow((1 + Rf),n));

constraint forall(n in floor(20 / dT)..floor(23 / dT))(x[n,TuitionB] = 40000 * pow((1 + Rf),n));

constraint forall(n in floor(22 / dT)..floor(25 / dT))(x[n,TuitionC] = 40000 * pow((1 + Rf),n));

constraint w[0] = Wi;

constraint forall(n in 1..Nper)(w[n] = (1 + Ri) * (w[n - 1] + u[n - 1]) - sum(e in EXPENSES)(x[n,e]));

constraint forall(n in 0..Nper)(u[n] <= fSave * salary[n]);



solve minimize fSave;




