set of int: BLOCK = 1..n;

array[INDEX_SET_shapeind] of set of int: shapeind = [if i = 1 then {j | j in 1..nemptycount[i]} else {j | j in floor(nemptycount[i - 1] + 1)..nemptycount[i]} endif | i in BLOCK];

set of int: ROFF = 1..m;

set of int: ROT = 1..4;

array[ROFF, 1..2] of int: rsize = array2d(ROFF,1..2,[d[i,j] | i in ROFF, j in 3..4]);

array[ROFF, 1..2] of int: roff = array2d(ROFF,1..2,[d[i,j] | i in ROFF, j in 1..2]);

array[int] of set of int: neshapeorient = [shapeorient[i] | i in 1..floor(n * 4) where shapeorient[i] != {}];

int: h;

int: n;

int: m;

array[BLOCK, ROT] of set of ROFF: shape;

array[ROFF, 1..4] of int: d;

array[BLOCK] of int: nemptycount = [sum(j in 1..floor(4 * i))(shapeorient[j] != {}) | i in BLOCK];

array[1..floor(n * 4)] of set of int: shapeorient = array1d([shape[i,j] | i in BLOCK, j in 1..4]);

int: maxl;


array[BLOCK, 1..2] of var int: coord;

array[BLOCK] of var int: kind;

array[BLOCK] of var 0..maxl: x;

var 0..maxl: l;

array[BLOCK] of var 0..h: y;

set of int: INDEX_SET_shapeind;


include "geost.mzn";

constraint forall(i in BLOCK)(coord[i,1] = x[i] /\ coord[i,2] = y[i]);

constraint forall(i in BLOCK)(kind[i] in shapeind[i]);

constraint geost_bb(2,rsize,roff,neshapeorient,coord,kind,[0,0],[l,h]);



solve minimize l;




