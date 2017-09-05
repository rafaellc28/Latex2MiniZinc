array[INDEX_SET_PAIRS, 1..2] of PEOPLE: PAIRS;

set of int: TABLES = 1..NTABLES;

set of int: PEOPLE = 1..TABLESIZE * NTABLES;

float: TABLESIZE = 3;

int: NTABLES = 4;

set of int: INDEX_SET_PAIRS;


array[int, int] of var bool: y;

array[int, int] of var bool: x;


constraint forall(p in PEOPLE)(sum(t in TABLES)(x[p,t]) = 1);

constraint forall(p in PEOPLE)((sum(q in 1..(p - 1))(y[q,p])) + (sum(q in (p + 1)..card(PEOPLE))(y[p,q])) = TABLESIZE - 1);

constraint forall(t in TABLES, p in INDEX_SET_PAIRS)(y[PAIRS[p,1],PAIRS[p,2]] >= x[PAIRS[p,1],t] + x[PAIRS[p,2],t] - 1);

constraint forall(t in TABLES)(sum(p in PEOPLE)(x[p,t]) = 3);



var float: obj = sum(p in INDEX_SET_PAIRS)(y[PAIRS[p,1],PAIRS[p,2]]);

solve maximize obj;




