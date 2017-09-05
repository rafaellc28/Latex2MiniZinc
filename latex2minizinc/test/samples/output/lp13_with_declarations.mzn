enum S;

set of int: H = 1..numhrs;

enum D;

array[int, int, int] of float: shifts;

array[int, int] of float: dmnd;

int: numhrs;


array[int] of var int: crew;


constraint forall(s in S)(crew[s] >= 0);

constraint forall(h in H, d in D)(sum(s in S)(crew[s] * shifts[d,h,s]) >= dmnd[h,d]);



var float: obj = sum(s in S)(crew[s]);

solve minimize obj;




