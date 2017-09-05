enum S;

enum H;

enum D;

array[int, int, int] of float: Shifts;

array[int, int] of float: Dmnd;


array[int] of var int: crew;


constraint forall(s in S)(crew[s] >= 0);

constraint forall(h in H, d in D)(sum(s in S)(crew[s] * Shifts[d,h,s]) >= Dmnd[h,d]);



var float: obj = sum(s in S)(crew[s]);

solve minimize obj;




