set of int: PLASTER = 1..total;

set of int: TYPE = 1..ntypes;

set of int: LENGTH = 1..length1;

set of int: WIDTH = 1..width;

enum USAGE = {Long,Wide,Not};

int: total = sum(number);

array[int] of int: t = [max(t in TYPE)(t * (p > psum[t])) | p in PLASTER];

array[int, int] of int: dim;

int: total_wounds = sum(array1d(wound));

int: length1;

int: width;

array[int, int] of bool: wound;

array[int] of int: number;

int: ntypes;

array[int] of int: price;

array[int] of int: psum = [sum(i in 1..floor(t - 1))(number[i]) | t in TYPE];

int: maxdim = max(array1d(dim));


array[INDEX_SET_covered_1, INDEX_SET_covered_2] of var bool: covered;

array[INDEX_SET_x_1] of var LENGTH: x;

array[INDEX_SET_y_1] of var WIDTH: y;

array[INDEX_SET_u_1] of var USAGE: u;

array[INDEX_SET_used_1] of var 0..max(number): used;

array[INDEX_SET_len_1] of var 0..maxdim: len = [[dim[t[p],1],dim[t[p],2],0][u[p]] | p in PLASTER];

array[INDEX_SET_wid_1] of var 0..maxdim: wid = [[dim[t[p],2],dim[t[p],1],0][u[p]] | p in PLASTER];

var int: cost = sum(t in TYPE)(used[t] * price[t]);

set of int: INDEX_SET_covered_1;

set of int: INDEX_SET_covered_2;

set of int: INDEX_SET_len_1;

set of int: INDEX_SET_u_1;

set of int: INDEX_SET_used_1;

set of int: INDEX_SET_wid_1;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_y_1;


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

constraint used[5] >= 1;

constraint used[2] >= 1;

constraint used[6] >= 1 -> exists(t in TYPE where [0,1,1,0,0,0][t] >= 1)(number[t] - used[t] < [0,1,1,0,0,0][t]);

constraint used[5] >= 1 -> exists(t in TYPE where [0,1,1,1,0,0][t] >= 1)(number[t] - used[t] < [0,1,1,1,0,0][t]);



solve minimize cost;




