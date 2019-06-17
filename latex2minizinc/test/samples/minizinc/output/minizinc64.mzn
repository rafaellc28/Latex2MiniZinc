enum WINE;

enum FOOD;

array[FOOD, WINE] of int: joy;


array[WINE] of var FOOD: eat;

array[FOOD] of var WINE: drink;


include "inverse.mzn";

constraint inverse(eat,drink);



solve maximize sum(w in WINE)(joy[eat[w],w]);




