enum ELEMENTS = {Metal,Wood,Water,Fire,Earth};

int: r = 3;

int: c = 2;

array[int, int] of ELEMENTS: compat;


array[INDEX_SET_herb_1, INDEX_SET_herb_2] of var ELEMENTS: herb;

array[INDEX_SET_rherb_1] of var ELEMENTS: rherb;

set of int: INDEX_SET_herb_1 = 1..r;

set of int: INDEX_SET_herb_2 = 1..c;

set of int: INDEX_SET_rherb_1 = 1..floor(r * c);


include "table.mzn";

include "global_cardinality_low_up.mzn";

constraint rherb = [array1d(herb)[r * c - i + 1] | i in 1..floor(r * c)];

constraint forall(i in 1..r, j in 1..floor(c - 1))(table([herb[i,j],herb[i,j + 1]],compat));

constraint forall(j in 1..c)(global_cardinality_low_up([herb[i,j] | i in 1..r],[Metal,Earth],[1,1],[2,2]));

constraint herb[1,1] != Metal;

solve satisfy;


