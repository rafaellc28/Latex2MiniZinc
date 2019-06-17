enum HERO;

enum SPOT;

array[HERO, SPOT] of int: damage;


array[HERO] of var SPOT: pos;

var int: tDamages = sum(h in HERO)(damage[h,pos[h]]);


include "alldifferent.mzn";

constraint alldifferent(pos);



solve maximize tDamages;




