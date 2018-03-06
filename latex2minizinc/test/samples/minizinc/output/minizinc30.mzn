set of int: GEN = 1..n;

set of int: ROAD = 1..n;

int: n;

array[int, int] of int: coop;


var int: scoop = sum(i in 1..floor(n - 1))(coop[road[i],road[i + 1]]);

array[INDEX_SET_road_1] of var GEN: road;

set of int: INDEX_SET_road_1;


include "alldifferent.mzn";

constraint alldifferent(road);

constraint road[1] < road[n];

constraint forall(i in 2..floor(n - 2))(forall(j in floor(i + 1)..floor(n - 1))(coop[road[i - 1],road[i]] + coop[road[j],road[j + 1]] >= coop[road[i - 1],road[j]] + coop[road[i],road[j + 1]]));



solve maximize scoop;




