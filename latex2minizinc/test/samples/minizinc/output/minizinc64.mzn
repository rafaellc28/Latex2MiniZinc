enum WINE;

enum FOOD;

array[int, int] of int: joy;


array[INDEX_SET_eat_1] of var FOOD: eat;

array[INDEX_SET_drink_1] of var WINE: drink;

set of int: INDEX_SET_drink_1 = FOOD;

set of int: INDEX_SET_eat_1 = WINE;


include "inverse.mzn";

constraint inverse(eat,drink);



solve maximize sum(w in WINE)(joy[eat[w],w]);




