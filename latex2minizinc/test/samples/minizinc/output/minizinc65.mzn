enum FOOD;

enum WINE;

array[int, int] of int: joy;


array[INDEX_SET_eat_1] of var FOOD: eat;

array[INDEX_SET_drink_1] of var WINE: drink;

set of int: INDEX_SET_drink_1;

set of int: INDEX_SET_eat_1;


include "alldifferent.mzn";

include "inverse.mzn";

constraint alldifferent(drink);

constraint alldifferent(eat);

constraint inverse(eat,drink);



solve maximize sum(f in FOOD)(joy[f,drink[f]]);




