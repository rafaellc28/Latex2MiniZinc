enum ELEMENTS = {Metal,Wood,Water,Fire,Earth};

array[1..r, 1..c] of ELEMENTS: compat;

int: r = 3;

int: c = 2;


array[1..r, 1..c] of var ELEMENTS: herb;


include "table.mzn";

include "global_cardinality_low_up.mzn";

constraint forall(i in 1..r, j in 1..floor(c - 1))(table([herb[i,j],herb[i,j + 1]],compat));

constraint forall(j in 1..c)(global_cardinality_low_up([herb[i,j] | i in 1..r],[Metal,Earth],[1,1],[2,2]));

constraint herb[1,1] != Metal;

solve satisfy;


