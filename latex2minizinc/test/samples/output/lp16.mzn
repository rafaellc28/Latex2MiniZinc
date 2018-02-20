array[INDEX_SET_PAIRS, 1..2] of PEOPLE: PAIRS;

enum TABLES;

enum PEOPLE;

float: TABLESIZE;


array[INDEX_SET_y_1, INDEX_SET_y_2] of var bool: y;

array[INDEX_SET_x_1, INDEX_SET_x_2] of var bool: x;

set of int: INDEX_SET_PAIRS;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;

set of int: INDEX_SET_y_1;

set of int: INDEX_SET_y_2;


constraint forall(p in PEOPLE)(sum(t in TABLES)(x[p,t]) = 1);

constraint forall(p in PEOPLE)((sum(q in 1..(p - 1))(y[to_enum(PEOPLE,q),p])) + (sum(q in (p + 1)..card(PEOPLE))(y[p,to_enum(PEOPLE,q)])) = TABLESIZE - 1);

constraint forall(t in TABLES, p in INDEX_SET_PAIRS)(y[PAIRS[p,1],PAIRS[p,2]] >= x[PAIRS[p,1],t] + x[PAIRS[p,2],t] - 1);

constraint forall(t in TABLES)(sum(p in PEOPLE)(x[p,t]) = 3);



solve maximize sum(p in INDEX_SET_PAIRS)(y[PAIRS[p,1],PAIRS[p,2]]);




