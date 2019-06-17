enum FOOD;

enum WINE;

array[FOOD, WINE] of int: joy;


array[FOOD] of var WINE: drink;


include "alldifferent.mzn";

constraint alldifferent(drink);



solve maximize sum(f in FOOD)(joy[f,drink[f]]);




