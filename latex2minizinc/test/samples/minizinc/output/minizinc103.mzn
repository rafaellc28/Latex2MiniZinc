int: size;

int: nPts;

int: mDist;

array[1..size, 1..size] of int: cost;


array[1..nPts] of var 1..size: ptR;

array[1..nPts] of var 1..size: ptC;

var int: tCost = sum(i in 1..nPts)(cost[ptR[i],ptC[i]]);


include "alldifferent.mzn";

constraint let {array[1..nPts] of var 1..floor(size * size): points = [(ptR[i] - 1) * size + ptC[i] | i in 1..nPts]} in
	alldifferent(points);

constraint forall(i in 1..nPts)((ptR[i] mod 2) = 1 \/ (ptR[i] mod 2) = 1);

predicate covered(var int: x, var int: y) =
	let {var 1..nPts: i; var int: dist = abs(x - ptR[i]) + abs(y - ptC[i])} in
	dist <= mDist;

constraint let {array[1..(size div 2)] of 1..floor(size - 1): huts = [i * 2 | i in 1..(size div 2)]} in
	forall(i,j in huts)(covered(i,j));



solve minimize tCost;




