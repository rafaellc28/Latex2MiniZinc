enum FOOD;

enum WINE;

array[FOOD, WINE] of int: joy;


array[WINE] of var FOOD: eat;

array[FOOD] of var WINE: drink;


include "alldifferent.mzn";

include "inverse.mzn";

constraint alldifferent(drink);

constraint alldifferent(eat);

constraint inverse(eat,drink);



solve maximize sum(f in FOOD)(joy[f,drink[f]]);




