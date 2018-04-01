enum PIVOT;

set of int: POS = 1..card(PIVOT);

set of int: PREC = 1..m;

PIVOT: first;

array[int] of PIVOT: prev;

array[int] of PIVOT: post;

int: m;

array[int] of int: coord;


array[INDEX_SET_order_1] of var POS: order;

array[INDEX_SET_route_1] of var PIVOT: route;

set of int: INDEX_SET_order_1;

set of int: INDEX_SET_route_1;


include "alldifferent.mzn";

include "inverse.mzn";

constraint route[1] = first;

constraint alldifferent(order);

constraint inverse(order,route);

constraint forall(i in 1..m)(order[prev[i]] < order[post[i]]);



solve minimize sum(j in 1..floor(card(PIVOT) - 1))(abs(coord[route[j + 1]] - coord[route[j]]));




