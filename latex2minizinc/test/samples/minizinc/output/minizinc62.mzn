enum FOOD;

enum WINE;

array[int, int] of int: joy;


array[INDEX_SET_drink_1] of var WINE: drink;

set of int: INDEX_SET_drink_1 = FOOD;


include "alldifferent.mzn";

constraint alldifferent(drink);



solve maximize sum(f in FOOD)(joy[f,drink[f]]);




