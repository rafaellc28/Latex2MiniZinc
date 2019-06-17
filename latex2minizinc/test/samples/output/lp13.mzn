enum S;

enum H;

enum D;

array[D, H, S] of float: Shifts;

array[H, D] of float: Dmnd;


array[S] of var int: crew;


constraint forall(s in S)(crew[s] >= 0);

constraint forall(h in H, d in D)(sum(s in S)(crew[s] * Shifts[d,h,s]) >= Dmnd[h,d]);



solve minimize sum(s in S)(crew[s]);




