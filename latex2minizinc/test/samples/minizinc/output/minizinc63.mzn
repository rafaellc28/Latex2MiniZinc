enum WINE;

enum FOOD;

array[FOOD, WINE] of int: joy;


array[WINE] of var FOOD: eat;


include "alldifferent.mzn";

constraint alldifferent(eat);



solve maximize sum(w in WINE)(joy[eat[w],w]);




