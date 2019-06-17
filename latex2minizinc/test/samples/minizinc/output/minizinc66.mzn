enum PIVOT;

set of int: POS = 1..card(PIVOT);

set of int: PREC = 1..m;

PIVOT: first;

array[PREC] of PIVOT: prev;

array[PREC] of PIVOT: post;

int: m;

array[PIVOT] of int: coord;


array[PIVOT] of var POS: order;

array[POS] of var PIVOT: route;


include "alldifferent.mzn";

include "inverse.mzn";

constraint route[1] = first;

constraint alldifferent(order);

constraint inverse(order,route);

constraint forall(i in 1..m)(order[prev[i]] < order[post[i]]);



solve minimize sum(j in 1..floor(card(PIVOT) - 1))(abs(coord[route[j + 1]] - coord[route[j]]));




