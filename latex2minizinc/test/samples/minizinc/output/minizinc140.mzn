set of int: COLOR = 1..N;

array[int, int] of 0..N: start;

int: digs = ceil(log(10.0, int2float(N)));

int: N;


array[INDEX_SET_cell_1, INDEX_SET_cell_2] of var COLOR: cell;

array[INDEX_SET_celllist_1] of var COLOR: celllist;

set of int: INDEX_SET_cell_1 = COLOR;

set of int: INDEX_SET_cell_2 = COLOR;

set of int: INDEX_SET_celllist_1 = 1..floor(N * N);


include "alldifferent.mzn";

constraint forall(i,j in COLOR)(if start[i,j] > 0 then cell[i,j] = start[i,j] else true endif);

constraint forall(i in COLOR)(alldifferent([cell[i,j] | j in COLOR]));

constraint forall(j in COLOR)(alldifferent([cell[i,j] | i in COLOR]));

solve satisfy;


