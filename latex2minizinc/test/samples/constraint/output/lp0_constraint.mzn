array[INDEX_SET_Neighbors, 1..2] of Countries: Neighbors;

set of int: Countries;

float: NumColors;


array[Countries] of var int: color;

set of int: INDEX_SET_Neighbors;


constraint forall(c in Countries)(color[c] <= NumColors /\ color[c] >= 1);

constraint forall(c1 in INDEX_SET_Neighbors)(color[Neighbors[c1,1]] != color[Neighbors[c1,2]]);

solve satisfy;


