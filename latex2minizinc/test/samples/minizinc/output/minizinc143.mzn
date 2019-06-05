set of int: ELEMENTS = {Gold,Wood,Water,Fire,Earth};

set of int: SEASONS = {Spring,Summer,Autumn,Winter};

array[int, int] of int: eCompat;

int: n = 20;

array[int, int] of (ELEMENTS union SEASONS): esCompat;

int: Gold = 1;

int: Wood = 2;

int: Water = 3;

int: Fire = 4;

int: Earth = 5;

int: Spring = 1;

int: Summer = 2;

int: Autumn = 3;

int: Winter = 4;

int: x;

int: y;


array[INDEX_SET_oHerbs_1] of var ELEMENTS: oHerbs;

array[INDEX_SET_eHerbs_1] of var SEASONS: eHerbs;

set of int: INDEX_SET_eHerbs_1 = 1..floor(n div 2);

set of int: INDEX_SET_oHerbs_1 = 1..floor(n div 2);


include "table.mzn";

constraint forall(i in 1..(n div 2 - 1))(table([oHerbs[i],oHerbs[i + 1]],eCompat));

constraint forall(i in 1..(n div 2 - 1))(table([oHerbs[i],eHerbs[i]],esCompat) /\ table([eHerbs[i],oHerbs[i + 1]],esCompat));

constraint if n mod 2 = 0 then table([oHerbs[n div 2],eHerbs[n div 2]],esCompat) else true endif;

solve satisfy;


