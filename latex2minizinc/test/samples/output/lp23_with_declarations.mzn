set of int: P = [PLANES[p,1]| p in INDEX_SET_PLANES];

array[INDEX_SET_N, 1..2] of LOCATIONS: N = CUSTOMERS_union_START_union_FINISH;

array[INDEX_SET_START, 1..2] of int: START = array2d(INDEX_SET_START, 1..2, [if idx2 = 1 then PLANES[p,1] else PLANES[p,2] endif | p in INDEX_SET_PLANES, idx2 in 1..2]);

array[INDEX_SET_FINISH, 1..2] of int: FINISH = array2d(INDEX_SET_FINISH, 1..2, [if idx2 = 1 then PLANES[p,1] else PLANES[p,3] endif | p in INDEX_SET_PLANES, idx2 in 1..2]);

array[INDEX_SET_CUSTOMERS, 1..2] of int: CUSTOMERS;

enum LOCATIONS;

array[INDEX_SET_PLANES, 1..3] of int: PLANES;

array[LOCATIONS, LOCATIONS] of float: gcdist = array2d(LOCATIONS, LOCATIONS, [2 * 6371 * atan(sqrt(alpha[a,b])/sqrt(1 - alpha[a,b])) | a in LOCATIONS, b in LOCATIONS]);

array[LOCATIONS] of float: lat;

array[LOCATIONS] of float: lng;

float: d2r = 3.1415926 / 180;

array[LOCATIONS, LOCATIONS] of float: alpha = array2d(LOCATIONS, LOCATIONS, [pow(sin(d2r * (lat[a] - lat[b]) / 2),2) + cos(d2r * lat[a]) * cos(d2r * lat[b]) * pow(sin(d2r * (lng[a] - lng[b]) / 2),2) | a in LOCATIONS, b in LOCATIONS]);


array[P, INDEX_SET_x_2, INDEX_SET_x_3, INDEX_SET_x_4, INDEX_SET_x_5] of var bool: x;

array[P, INDEX_SET_y_2, INDEX_SET_y_3, INDEX_SET_y_4, INDEX_SET_y_5] of var int: y;

array[P] of var float: routeDistance;

array[P] of var float: routeLegs;

var float: maxDistance;

var float: maxLegs;

array[INDEX_SET_CUSTOMERS_union_FINISH,1..2] of int: CUSTOMERS_union_FINISH;

array[INDEX_SET_CUSTOMERS_union_START,1..2] of int: CUSTOMERS_union_START;

array[INDEX_SET_CUSTOMERS_union_START_union_FINISH,1..2] of int: CUSTOMERS_union_START_union_FINISH;

set of int: INDEX_SET_CUSTOMERS;

set of int: INDEX_SET_CUSTOMERS_union_FINISH;

set of int: INDEX_SET_CUSTOMERS_union_START;

set of int: INDEX_SET_CUSTOMERS_union_START_union_FINISH;

set of int: INDEX_SET_FINISH;

set of int: INDEX_SET_N;

set of int: INDEX_SET_PLANES;

set of int: INDEX_SET_START;

set of int: INDEX_SET_START_union_CUSTOMERS;

set of int: INDEX_SET_x_2 = N;

set of int: INDEX_SET_x_3 = N;

set of int: INDEX_SET_x_4;

set of int: INDEX_SET_x_5;

set of int: INDEX_SET_y_2 = N;

set of int: INDEX_SET_y_3 = N;

set of int: INDEX_SET_y_4;

set of int: INDEX_SET_y_5;

array[INDEX_SET_START_union_CUSTOMERS,1..2] of int: START_union_CUSTOMERS;


constraint forall(p in P, a in INDEX_SET_N, b in INDEX_SET_N)(y[p,N[a,1],N[a,2],N[b,1],N[b,2]] >= 0);

constraint forall(p in P)(routeDistance[p] >= 0);

constraint forall(p in P)(routeLegs[p] >= 0);

constraint maxDistance >= 0;

constraint maxLegs >= 0;

constraint forall(p in P, a in INDEX_SET_N, b in INDEX_SET_START)(x[p,N[a,1],N[a,2],START[b,1],START[b,2]] = 0);

constraint forall(p in P, a in INDEX_SET_FINISH, b in INDEX_SET_N)(x[p,FINISH[a,1],FINISH[a,2],N[b,1],N[b,2]] = 0);

constraint forall(p in P, a in INDEX_SET_START, b in INDEX_SET_N where p != START[a,1])(x[p,START[a,1],START[a,2],N[b,1],N[b,2]] = 0);

constraint forall(p in P, a in INDEX_SET_N, b in INDEX_SET_FINISH where p != FINISH[b,1])(x[p,N[a,1],N[a,2],FINISH[b,1],FINISH[b,2]] = 0);

constraint forall(b in INDEX_SET_CUSTOMERS_union_FINISH)(sum(p in P, a in INDEX_SET_CUSTOMERS_union_START)(x[p,CUSTOMERS_union_START[a,1],CUSTOMERS_union_START[a,2],CUSTOMERS_union_FINISH[b,1],CUSTOMERS_union_FINISH[b,2]]) = 1);

constraint forall(a in INDEX_SET_START_union_CUSTOMERS)(sum(p in P, b in INDEX_SET_CUSTOMERS_union_FINISH)(x[p,START_union_CUSTOMERS[a,1],START_union_CUSTOMERS[a,2],CUSTOMERS_union_FINISH[b,1],CUSTOMERS_union_FINISH[b,2]]) = 1);

constraint forall(p in P, a in INDEX_SET_CUSTOMERS)(sum(b in INDEX_SET_CUSTOMERS_union_START)(x[p,CUSTOMERS_union_START[b,1],CUSTOMERS_union_START[b,2],CUSTOMERS[a,1],CUSTOMERS[a,2]]) = sum(b in INDEX_SET_CUSTOMERS_union_FINISH)(x[p,CUSTOMERS[a,1],CUSTOMERS[a,2],CUSTOMERS_union_FINISH[b,1],CUSTOMERS_union_FINISH[b,2]]));

constraint forall(p in P, a in INDEX_SET_N, b in INDEX_SET_N where (N[a,1] = N[b,1]) /\ (N[a,2] = N[b,2]))(x[p,N[a,1],N[a,2],N[b,1],N[b,2]] = 0);

constraint forall(p in P, a in INDEX_SET_N, b in INDEX_SET_N)(y[p,N[a,1],N[a,2],N[b,1],N[b,2]] <= card(INDEX_SET_CUSTOMERS) * x[p,N[a,1],N[a,2],N[b,1],N[b,2]]);

constraint sum(p in P, a in INDEX_SET_START, b in INDEX_SET_N)(y[p,START[a,1],START[a,2],N[b,1],N[b,2]]) = card(INDEX_SET_CUSTOMERS);

constraint forall(a in INDEX_SET_CUSTOMERS)(sum(p in P, b in INDEX_SET_CUSTOMERS_union_START)(y[p,CUSTOMERS_union_START[b,1],CUSTOMERS_union_START[b,2],CUSTOMERS[a,1],CUSTOMERS[a,2]]) = 1 + sum(p in P, b in INDEX_SET_CUSTOMERS_union_FINISH)(y[p,CUSTOMERS[a,1],CUSTOMERS[a,2],CUSTOMERS_union_FINISH[b,1],CUSTOMERS_union_FINISH[b,2]]));

constraint forall(p in P)(routeDistance[p] = sum(a in INDEX_SET_N, b in INDEX_SET_N)(gcdist[N[a,2],N[b,2]] * x[p,N[a,1],N[a,2],N[b,1],N[b,2]]));

constraint forall(p in P)(routeLegs[p] = sum(a in INDEX_SET_START, b in INDEX_SET_N)(y[p,START[a,1],START[a,2],N[b,1],N[b,2]]));

constraint forall(p in P)(routeDistance[p] <= maxDistance);

constraint forall(p in P)(routeLegs[p] <= maxLegs);



solve minimize sum(p in P)(routeDistance[p]);




