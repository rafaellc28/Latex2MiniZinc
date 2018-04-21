set of int: STEP = 1..maxstep;

set of int: NODE = 1..n;

set of int: EDGE = 1..m;

int: start;

int: dest;

array[int, int] of int: uedge = array2d(1..floor(2 * m),1..2,[edge[i,j] | i in EDGE, j in 1..2] ++ [edge[i,3 - j] | i in EDGE, j in 1..2]);

int: maxstep;

int: rest;

array[int] of int: guard;

int: n;

int: m;

array[int, int] of int: edge;


var STEP: step;

array[INDEX_SET_path_1] of var NODE: path;

set of int: INDEX_SET_path_1;


include "table.mzn";

include "sliding_sum.mzn";

constraint path[1] = start;

constraint forall(i in STEP)(i >= step -> path[i] = dest);

constraint forall(i in 1..floor(maxstep - 1))(table([path[i],path[i + 1]],uedge));

constraint sliding_sum(1,rest,rest,[guard[path[i]] = 0 | i in STEP]);

constraint forall(e in EDGE, i in 1..2)(edge[e,i] in NODE);



solve minimize sum(i in STEP)(guard[path[i]]);




