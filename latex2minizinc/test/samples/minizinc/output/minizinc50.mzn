set of int: BLOCK = 1..n;

array[INDEX_SET_shapeind] of set of int: shapeind;

set of int: ROFF = 1..m;

array[int, int] of int: rsize = array2d(ROFF,1..2,[d[i,j] | i in ROFF, j in 3..4]);

array[int, int] of int: roff = array2d(ROFF,1..2,[d[i,j] | i in ROFF, j in 1..2]);

array[int] of set of ROFF: shape;

int: h;

int: n;

int: m;

array[int, int] of int: d;

int: maxl;


array[INDEX_SET_coord_1, INDEX_SET_coord_2] of var int: coord;

array[INDEX_SET_kind_1] of var int: kind;

array[INDEX_SET_x_1] of var 0..maxl: x;

var 0..maxl: l;

array[INDEX_SET_y_1] of var 0..h: y;

set of int: INDEX_SET_coord_1;

set of int: INDEX_SET_coord_2 = 1..2;

set of int: INDEX_SET_kind_1;

set of int: INDEX_SET_shapeind;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_y_1;


include "geost.mzn";

constraint forall(i in BLOCK)(coord[i,1] = x[i] /\ coord[i,2] = y[i]);

constraint forall(i in BLOCK)(kind[i] in shapeind[i]);

constraint geost_bb(2,rsize,roff,shape,coord,kind,[0,0],[l,h]);



solve minimize l;




