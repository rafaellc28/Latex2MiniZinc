set of int: COLOR = 1..N;

array[COLOR, COLOR] of 0..N: start;

int: digs = ceil(log(10.0, int2float(N)));

int: N;


array[COLOR, COLOR] of var COLOR: cell;

array[1..floor(N * N)] of var COLOR: celllist;


include "alldifferent.mzn";

constraint forall(i,j in COLOR)(if start[i,j] > 0 then cell[i,j] = start[i,j] else true endif);

constraint forall(i in COLOR)(alldifferent([cell[i,j] | j in COLOR]));

constraint forall(j in COLOR)(alldifferent([cell[i,j] | i in COLOR]));

solve satisfy;


