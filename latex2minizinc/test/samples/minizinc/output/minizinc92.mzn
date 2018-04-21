set of int: STEP = 1..maxstep;

set of int: NODE = 1..n;

set of int: EDGE = 1..m;

int: start;

int: dest;

array[int, int] of int: edge;

int: maxstep;

int: rest;

array[int] of int: guard;

int: n;

int: m;


var STEP: step;

array[INDEX_SET_path_1] of var NODE: path;

set of int: INDEX_SET_path_1;


include "table.mzn";

include "sliding_sum.mzn";

constraint path[1] = start;

constraint forall(i in STEP)(i >= step -> path[i] = dest);

constraint forall(i in 1..floor(maxstep - 1))(table([path[i],path[i + 1]],edge));

constraint sliding_sum(1,rest,rest,[guard[path[i]] = 0 | i in STEP]);



solve minimize sum(i in STEP)(guard[path[i]]);




