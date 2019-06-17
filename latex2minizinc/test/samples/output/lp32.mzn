enum EXPENSES;

enum N;

array[N] of float: Salary;

float: Rf;

float: DT;

float: Wi;

float: Ri;

N: Nper;


var float: fSave;

array[N] of var float: w;

array[1..Nper, EXPENSES] of var float: x;

array[N] of var float: u;

EXPENSES: TuitionA;

EXPENSES: TuitionB;

EXPENSES: TuitionC;


constraint forall(n in N)(w[n] >= 0);

constraint forall(n in 1..Nper, e in EXPENSES)(x[n,e] >= 0);

constraint forall(n in N)(u[n] >= 0);

constraint w[Nper] = 8 * Salary[Nper];

constraint forall(n in floor(18 / DT)..floor(21 / DT))(x[n,TuitionA] = 40000 * pow((1 + Rf),n));

constraint forall(n in floor(20 / DT)..floor(23 / DT))(x[n,TuitionB] = 40000 * pow((1 + Rf),n));

constraint forall(n in floor(22 / DT)..floor(25 / DT))(x[n,TuitionC] = 40000 * pow((1 + Rf),n));

constraint w[to_enum(N,0)] = Wi;

constraint forall(n in 1..Nper)(w[to_enum(N,n)] = (1 + Ri) * (w[to_enum(N,to_enum(N,n) - 1)] + u[to_enum(N,to_enum(N,n) - 1)]) - sum(e in EXPENSES)(x[n,e]));

constraint forall(n in 0..Nper)(u[to_enum(N,n)] <= fSave * Salary[to_enum(N,n)]);

constraint forall(n in N)(u[n] >= 0);

constraint forall(n in N)(w[n] >= 0);

constraint forall(n in N)(Salary[n] >= 0);



solve minimize fSave;




