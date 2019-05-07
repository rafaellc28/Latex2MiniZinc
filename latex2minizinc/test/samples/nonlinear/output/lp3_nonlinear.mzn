array[INDEX_SET_PAIRS, 1..2] of int: PAIRS;

set of int: J = 1..18;

set of int: I = 1..16;

set of int: K = 1..17;

array[int, int] of float: c;

array[int, int, int] of float: E;

array[int] of float: b;

float: xlb;


array[INDEX_SET_x_1, INDEX_SET_x_2] of var float: x;

set of int: INDEX_SET_PAIRS;

set of int: INDEX_SET_x_1 = PAIRS;

set of int: INDEX_SET_x_2;


constraint forall(i in I)(assert(b[i] >= 0, "Assertion b[\(i)] >= 0 failed!"));

constraint assert(xlb >= 0, "Assertion xlb >= 0 failed!");

constraint forall(j in INDEX_SET_PAIRS)(x[PAIRS[j,1],PAIRS[j,2]] >= xlb);

constraint forall(i in I)(sum(j in INDEX_SET_PAIRS)(E[PAIRS[j,1],PAIRS[j,2],i] * x[PAIRS[j,1],PAIRS[j,2]] - b[i]) = 0);



solve minimize sum(j in INDEX_SET_PAIRS)(x[PAIRS[j,1],PAIRS[j,2]] * (c[PAIRS[j,1],PAIRS[j,2]] + log(x[PAIRS[j,1],PAIRS[j,2]] / sum(m in J where m in INDEX_SET_PAIRS)(x[m,PAIRS[j,2]]))));




