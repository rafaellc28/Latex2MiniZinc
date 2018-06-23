enum S;

enum H;

enum D;

array[int, int, int] of float: Shifts;

array[int, int] of float: Dmnd;


array[INDEX_SET_crew_1] of var int: crew;

set of int: INDEX_SET_crew_1 = S;


constraint forall(s in INDEX_SET_crew_1)(crew[s] >= 0);

constraint forall(h in H, d in D)(sum(s in S)(crew[s] * Shifts[d,h,s]) >= Dmnd[h,d]);



solve minimize sum(s in S)(crew[s]);




