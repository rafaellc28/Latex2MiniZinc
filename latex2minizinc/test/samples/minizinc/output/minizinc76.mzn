enum HERO;

enum SPOT;

array[int, int] of int: damage;


array[INDEX_SET_pos_1] of var SPOT: pos;

var int: tDamages = sum(h in HERO)(damage[h,pos[h]]);

set of int: INDEX_SET_pos_1;


include "alldifferent.mzn";

constraint alldifferent(pos);



solve maximize tDamages;




