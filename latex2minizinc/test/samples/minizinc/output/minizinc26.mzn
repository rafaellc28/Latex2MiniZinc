set of int: COL = 1..b;

set of int: ROW = 1..v;

int: r;

int: k;

int: lambda;

int: v;

int: b;


array[ROW, COL] of var bool: m;


constraint forall(i in ROW)(sum(j in COL)(m[i,j]) = r);

constraint forall(j in COL)(sum(i in ROW)(m[i,j]) = k);

constraint forall(i1,i2 in ROW where i1 < i2)(sum(j in COL)(m[i1,j] = true /\ m[i2,j] = true) = lambda);

solve satisfy;


