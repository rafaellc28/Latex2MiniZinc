array[INDEX_SET_P, 1..2] of int: P;

set of int: D = 1..d;

set of int: I = 1..N;

int: d;

int: N;


array[INDEX_SET_x_1, INDEX_SET_x_2] of var float: x;

array[INDEX_SET_r_1, INDEX_SET_r_2] of var float: r;

set of int: INDEX_SET_P;

set of int: INDEX_SET_r_1;

set of int: INDEX_SET_r_2;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;


constraint forall(i in INDEX_SET_P)(r[P[i,1],P[i,2]] = sqrt(sum(k in D)(pow((x[P[i,1],k] - x[P[i,2],k]),2))));





solve minimize sum(i in INDEX_SET_P)((pow(r[P[i,1],P[i,2]],-12) - 2 * pow(r[P[i,1],P[i,2]],-6)));




