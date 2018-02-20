enum S;

set of int: H = 1..numhrs;

enum D;

array[int, int, int] of float: shifts;

array[int, int] of float: dmnd;

int: numhrs;


array[INDEX_SET_crew_1] of var int: crew;

set of int: INDEX_SET_crew_1;


constraint forall(s in S)(crew[s] >= 0);

constraint forall(h in H, d in D)(sum(s in S)(crew[s] * shifts[d,h,s]) >= dmnd[h,d]);



solve minimize sum(s in S)(crew[s]);




