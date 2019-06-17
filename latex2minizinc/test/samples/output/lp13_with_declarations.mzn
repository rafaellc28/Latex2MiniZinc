enum S;

set of int: H = 1..numhrs;

enum D;

array[D, H, S] of float: shifts;

array[H, D] of float: dmnd;

int: numhrs;


array[S] of var int: crew;


constraint forall(s in S)(crew[s] >= 0);

constraint forall(h in H, d in D)(sum(s in S)(crew[s] * shifts[d,h,s]) >= dmnd[h,d]);



solve minimize sum(s in S)(crew[s]);




