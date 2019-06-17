set of int: GEN = 1..n;

set of int: ROAD = 1..n;

int: n;

array[GEN, GEN] of int: coop;


var int: scoop = sum(i in 1..floor(n - 1))(coop[road[i],road[i + 1]]);

array[ROAD] of var GEN: road;


include "alldifferent.mzn";

constraint alldifferent(road);

constraint road[1] < road[n];



solve maximize scoop;




