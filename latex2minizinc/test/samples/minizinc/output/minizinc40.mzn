set of int: PLASTER = 1..total;

set of int: TYPE = 1..ntypes;

set of int: LENGTH = 1..length1;

set of int: WIDTH = 1..width;

enum USAGE = {Long,Wide,Not};

int: total = sum(number);

array[PLASTER] of int: t = [max(t in TYPE)(t * (p > psum[t])) | p in PLASTER];

array[TYPE, 1..2] of int: dim;

int: total_wounds = sum(array1d(wound));

int: length1;

int: width;

array[LENGTH, WIDTH] of bool: wound;

int: ntypes;

array[TYPE] of int: number;

array[TYPE] of int: price;

array[TYPE] of int: psum = [sum(i in 1..floor(t - 1))(number[i]) | t in TYPE];

int: maxdim = max(array1d(dim));


array[LENGTH, WIDTH] of var bool: covered;

array[PLASTER] of var LENGTH: x;

array[PLASTER] of var WIDTH: y;

array[PLASTER] of var USAGE: u;

array[TYPE] of var 0..max(number): used;

array[PLASTER] of var 0..maxdim: len = [[dim[t[p],1],dim[t[p],2],0][u[p]] | p in PLASTER];

array[PLASTER] of var 0..maxdim: wid = [[dim[t[p],2],dim[t[p],1],0][u[p]] | p in PLASTER];

var int: cost = sum(t in TYPE)(used[t] * price[t]);


include "lex_lesseq.mzn";

include "diffn.mzn";

constraint forall(p in 1..floor(total - 1) where t[p] = t[p + 1])(lex_lesseq([u[p],x[p],y[p]],[u[p + 1],x[p + 1],y[p + 1]]));

constraint forall(p in PLASTER)(u[p] = Not -> x[p] = 1 /\ y[p] = 1);

constraint forall(ty in TYPE)(used[ty] = sum(p in PLASTER where t[p] = ty)(u[p] != Not));

constraint sum(ty in TYPE)(used[ty] * dim[ty,1] * dim[ty,2]) >= total_wounds;

constraint forall(p in PLASTER)(if dim[t[p],1] = dim[t[p],2] then u[p] != Wide else true endif);

constraint diffn(x,y,len,wid);

constraint forall(p in PLASTER)(x[p] + len[p] - 1 <= length1 /\ y[p] + wid[p] - 1 <= width);

constraint forall(p in PLASTER)(u[p] != Not -> (forall(i in LENGTH, j in WIDTH)(((x[p] <= i /\ x[p] + len[p] > i /\ y[p] <= j /\ y[p] + wid[p] > j) -> (covered[i,j])))));

constraint forall(i in LENGTH, j in WIDTH)(covered[i,j] = true -> exists(p in PLASTER)((x[p] <= i /\ x[p] + len[p] > i /\ y[p] <= j /\ y[p] + wid[p] > j)));

constraint forall(i in LENGTH, j in WIDTH)(wound[i,j] = true -> covered[i,j] = true);



solve minimize cost;




