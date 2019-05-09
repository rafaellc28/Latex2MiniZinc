enum ELEMENTS = {Gold,Wood,Water,Fire,Earth};

array[int, int] of ELEMENTS: eCompat;

int: n = 20;

int: k;


array[INDEX_SET_herb_1] of var ELEMENTS: herb;

set of int: INDEX_SET_herb_1 = 1..n;


constraint assert(k = 4, "Assertion k = 4 failed!");

include "table.mzn";

include "global_cardinality_low_up.mzn";

constraint forall(i in 1..(n - 1))(table([herb[i],herb[i + 1]],eCompat));

constraint forall(i in 1..floor(n - 3))(herb[i] != herb[i + 3]);

constraint forall(i in 1..floor(n - k + 1))(global_cardinality_low_up([herb[i + j - 1] | j in 1..k],[Gold,Earth],[1,1],[2,2]));

constraint herb[1] != Gold;

solve satisfy;


