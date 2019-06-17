enum BATTALION = {B1,B2,B3,B4,B5,B6,B7,B8,B9,B10,B11,B12,B13,B14,B15,B16,B17,B18,B19,B20,B21,B22,B23,B24};

set of BATTALION: ARCHER = {B1,B2,B3,B4,B15};

set of BATTALION: SWORD = {B3,B8,B9,B6,B15};

set of BATTALION: SHIELD = {B1,B3,B15,B16,B18};

set of int: BRIGADE = 1..nbrigade;

int: size = 6;

int: nbrigade = floor(card(BATTALION)) div size;


array[BRIGADE] of var set of BATTALION: brigades;

set of int: INDEX_SET_t;


include "all_disjoint.mzn";

include "alldifferent.mzn";

constraint forall(i in 1..nbrigade)(card(brigades[i]) = size);

constraint all_disjoint(brigades);

predicate alldifferent(array[int] of var BATTALION: b) =
	forall(i,j in index_set(b) where i < j)(b[i] != b[j]);

predicate pattern(var set of BATTALION: brigade, array[int] of var set of BATTALION: t) =
	let {set of int: IND = 1..length(t); array[IND] of var BATTALION: b} in
	forall(i in IND)((b[i] in t[i] /\ b[i] in brigade) /\ alldifferent(b));

predicate elite(var set of BATTALION: brigade) =
	pattern(brigade,[ARCHER,ARCHER,SHIELD,SHIELD]) \/ pattern(brigade,[SWORD,SWORD,SWORD]) \/ pattern(brigade,[ARCHER,SWORD,SWORD,SHIELD]);

constraint elite(brigades[1]);

constraint elite(brigades[2]);

solve satisfy;


