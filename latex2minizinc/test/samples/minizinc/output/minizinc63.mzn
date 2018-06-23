enum WINE;

enum FOOD;

array[int, int] of int: joy;


array[INDEX_SET_eat_1] of var FOOD: eat;

set of int: INDEX_SET_eat_1 = WINE;


include "alldifferent.mzn";

constraint alldifferent(eat);



solve maximize sum(w in WINE)(joy[eat[w],w]);




