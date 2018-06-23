enum P;

array[INDEX_SET_N, 1..2] of LOCATIONS: N;

array[INDEX_SET_START, 1..2] of int: START;

array[INDEX_SET_FINISH, 1..2] of int: FINISH;

array[INDEX_SET_CUSTOMERS, 1..2] of int: CUSTOMERS;

enum LOCATIONS;

float: Maxspeed;

array[int, int] of float: Gcdist;

float: BigM;

float: Minspeed;

array[int, int] of float: T1;

array[int, int] of float: TF1;

array[int, int] of float: T2;

array[int, int] of float: TF2;

array[int, int] of float: TS1;

array[int, int] of float: TS2;


var float: timePenalty;

var float: totalDistance;

array[INDEX_SET_tlv_1, INDEX_SET_tlv_2] of var float: tlv;

array[INDEX_SET_tar_1, INDEX_SET_tar_2] of var float: tar;

array[INDEX_SET_tea_1, INDEX_SET_tea_2] of var float: tea;

array[INDEX_SET_tla_1, INDEX_SET_tla_2] of var float: tla;

array[INDEX_SET_ted_1, INDEX_SET_ted_2] of var float: ted;

array[INDEX_SET_tld_1, INDEX_SET_tld_2] of var float: tld;

array[INDEX_SET_routeDistance_1] of var float: routeDistance;

array[INDEX_SET_x_1, INDEX_SET_x_2, INDEX_SET_x_3, INDEX_SET_x_4, INDEX_SET_x_5] of var bool: x;

array[INDEX_SET_y_1, INDEX_SET_y_2, INDEX_SET_y_3, INDEX_SET_y_4, INDEX_SET_y_5] of var float: y;

array[INDEX_SET_CUSTOMERS_union_FINISH,1..2] of int: CUSTOMERS_union_FINISH;

array[INDEX_SET_CUSTOMERS_union_START,1..2] of int: CUSTOMERS_union_START;

set of int: INDEX_SET_CUSTOMERS;

set of int: INDEX_SET_CUSTOMERS_union_FINISH;

set of int: INDEX_SET_CUSTOMERS_union_START;

set of int: INDEX_SET_FINISH;

set of int: INDEX_SET_N;

set of int: INDEX_SET_START;

set of int: INDEX_SET_START_union_CUSTOMERS;

set of int: INDEX_SET_routeDistance_1 = P;

set of int: INDEX_SET_tar_1 = N;

set of int: INDEX_SET_tar_2;

set of int: INDEX_SET_tea_1 = N;

set of int: INDEX_SET_tea_2;

set of int: INDEX_SET_ted_1 = N;

set of int: INDEX_SET_ted_2;

set of int: INDEX_SET_tla_1 = N;

set of int: INDEX_SET_tla_2;

set of int: INDEX_SET_tld_1 = N;

set of int: INDEX_SET_tld_2;

set of int: INDEX_SET_tlv_1 = N;

set of int: INDEX_SET_tlv_2;

set of int: INDEX_SET_x_1 = P;

set of int: INDEX_SET_x_2 = N;

set of int: INDEX_SET_x_3 = N;

set of int: INDEX_SET_x_4;

set of int: INDEX_SET_x_5;

set of int: INDEX_SET_y_1 = P;

set of int: INDEX_SET_y_2 = N;

set of int: INDEX_SET_y_3 = N;

set of int: INDEX_SET_y_4;

set of int: INDEX_SET_y_5;

array[INDEX_SET_START_union_CUSTOMERS,1..2] of int: START_union_CUSTOMERS;


constraint timePenalty >= 0;

constraint totalDistance >= 0;

constraint forall(a in INDEX_SET_N)(tea[N[a,1],N[a,2]] >= 0);

constraint forall(a in INDEX_SET_N)(tla[N[a,1],N[a,2]] >= 0);

constraint forall(a in INDEX_SET_N)(ted[N[a,1],N[a,2]] >= 0);

constraint forall(a in INDEX_SET_N)(tld[N[a,1],N[a,2]] >= 0);

constraint forall(p in INDEX_SET_routeDistance_1)(routeDistance[p] >= 0);

constraint forall(p in INDEX_SET_y_1, a in INDEX_SET_N, b in INDEX_SET_N)(y[p,N[a,1],N[a,2],N[b,1],N[b,2]] >= 0);

constraint forall(p in P, a in INDEX_SET_N, b in INDEX_SET_START)(x[p,N[a,1],N[a,2],START[b,1],START[b,2]] = 0);

constraint forall(p in P, a in INDEX_SET_FINISH, b in INDEX_SET_N)(x[p,FINISH[a,1],FINISH[a,2],N[b,1],N[b,2]] = 0);

constraint forall(p in P, a in INDEX_SET_START, b in INDEX_SET_N where p != START[a,1])(x[p,START[a,1],START[a,2],N[b,1],N[b,2]] = 0);

constraint forall(p in P, a in INDEX_SET_N, b in INDEX_SET_FINISH where p != FINISH[b,1])(x[p,N[a,1],N[a,2],FINISH[b,1],FINISH[b,2]] = 0);

constraint forall(b in INDEX_SET_CUSTOMERS_union_FINISH)(sum(p in P, a in INDEX_SET_CUSTOMERS_union_START)(x[p,CUSTOMERS_union_START[a,1],CUSTOMERS_union_START[a,2],CUSTOMERS_union_FINISH[b,1],CUSTOMERS_union_FINISH[b,2]]) = 1);

constraint forall(a in INDEX_SET_START_union_CUSTOMERS)(sum(p in P, b in INDEX_SET_CUSTOMERS_union_FINISH)(x[p,START_union_CUSTOMERS[a,1],START_union_CUSTOMERS[a,2],CUSTOMERS_union_FINISH[b,1],CUSTOMERS_union_FINISH[b,2]]) = 1);

constraint forall(p in P, a in INDEX_SET_CUSTOMERS)(sum(b in INDEX_SET_CUSTOMERS_union_START)(x[p,CUSTOMERS_union_START[b,1],CUSTOMERS_union_START[b,2],CUSTOMERS[a,1],CUSTOMERS[a,2]]) = sum(b in INDEX_SET_CUSTOMERS_union_FINISH)(x[p,CUSTOMERS[a,1],CUSTOMERS[a,2],CUSTOMERS_union_FINISH[b,1],CUSTOMERS_union_FINISH[b,2]]));

constraint forall(p in P, a in INDEX_SET_N, b in INDEX_SET_N where (N[a,1] = N[b,1]) /\ (N[a,2] = N[b,2]))(x[p,N[a,1],N[a,2],N[b,1],N[b,2]] = 0);

constraint sum(p in P, a in INDEX_SET_START, b in INDEX_SET_N)(y[p,START[a,1],START[a,2],N[b,1],N[b,2]]) = card(INDEX_SET_CUSTOMERS);

constraint forall(a in INDEX_SET_CUSTOMERS)(sum(p in P, b in INDEX_SET_CUSTOMERS_union_START)(y[p,CUSTOMERS_union_START[b,1],CUSTOMERS_union_START[b,2],CUSTOMERS[a,1],CUSTOMERS[a,2]]) = 1 + sum(p in P, b in INDEX_SET_CUSTOMERS_union_FINISH)(y[p,CUSTOMERS[a,1],CUSTOMERS[a,2],CUSTOMERS_union_FINISH[b,1],CUSTOMERS_union_FINISH[b,2]]));

constraint forall(a in INDEX_SET_N)(tlv[N[a,1],N[a,2]] >= tar[N[a,1],N[a,2]]);

constraint forall(p in P, a in INDEX_SET_N, b in INDEX_SET_N)(tar[N[b,1],N[b,2]] >= tlv[N[a,1],N[a,2]] + Gcdist[N[a,2],N[b,2]] / Maxspeed - BigM * (1 - x[p,N[a,1],N[a,2],N[b,1],N[b,2]]));

constraint forall(p in P, a in INDEX_SET_N, b in INDEX_SET_N)(tar[N[b,1],N[b,2]] <= tlv[N[a,1],N[a,2]] + Gcdist[N[a,2],N[b,2]] / Minspeed + BigM * (1 - x[p,N[a,1],N[a,2],N[b,1],N[b,2]]));

constraint forall(a in INDEX_SET_CUSTOMERS)(tea[CUSTOMERS[a,1],CUSTOMERS[a,2]] >= T1[CUSTOMERS[a,1],CUSTOMERS[a,2]] - tar[CUSTOMERS[a,1],CUSTOMERS[a,2]]);

constraint forall(a in INDEX_SET_FINISH)(tea[FINISH[a,1],FINISH[a,2]] >= TF1[FINISH[a,1],FINISH[a,2]] - tar[FINISH[a,1],FINISH[a,2]]);

constraint forall(a in INDEX_SET_CUSTOMERS)(tla[CUSTOMERS[a,1],CUSTOMERS[a,2]] >= tar[CUSTOMERS[a,1],CUSTOMERS[a,2]] - T2[CUSTOMERS[a,1],CUSTOMERS[a,2]]);

constraint forall(a in INDEX_SET_FINISH)(tla[FINISH[a,1],FINISH[a,2]] >= tar[FINISH[a,1],FINISH[a,2]] - TF2[FINISH[a,1],FINISH[a,2]]);

constraint forall(a in INDEX_SET_START)(ted[START[a,1],START[a,2]] >= TS1[START[a,1],START[a,2]] - tlv[START[a,1],START[a,2]]);

constraint forall(a in INDEX_SET_CUSTOMERS)(ted[CUSTOMERS[a,1],CUSTOMERS[a,2]] >= T1[CUSTOMERS[a,1],CUSTOMERS[a,2]] - tlv[CUSTOMERS[a,1],CUSTOMERS[a,2]]);

constraint forall(a in INDEX_SET_START)(tld[START[a,1],START[a,2]] >= tlv[START[a,1],START[a,2]] - TS2[START[a,1],START[a,2]]);

constraint forall(a in INDEX_SET_CUSTOMERS)(tld[CUSTOMERS[a,1],CUSTOMERS[a,2]] >= tlv[CUSTOMERS[a,1],CUSTOMERS[a,2]] - T2[CUSTOMERS[a,1],CUSTOMERS[a,2]]);

constraint forall(p in P)(routeDistance[p] = sum(a in INDEX_SET_N, b in INDEX_SET_N)(Gcdist[N[a,2],N[b,2]] * x[p,N[a,1],N[a,2],N[b,1],N[b,2]]));

constraint totalDistance = sum(p in P)(routeDistance[p]);

constraint timePenalty = sum(a in INDEX_SET_N)((tea[N[a,1],N[a,2]] + 2 * tla[N[a,1],N[a,2]] + 2 * ted[N[a,1],N[a,2]] + tld[N[a,1],N[a,2]]));

constraint forall(p in P, a in INDEX_SET_N, b in INDEX_SET_N)(y[p,N[a,1],N[a,2],N[b,1],N[b,2]] <= card(INDEX_SET_CUSTOMERS) * x[p,N[a,1],N[a,2],N[b,1],N[b,2]]);

constraint forall(a in LOCATIONS, b in LOCATIONS)(Gcdist[a,b] >= 0);

constraint forall(a in INDEX_SET_N)(tlv[N[a,1],N[a,2]] >= 0);

constraint forall(a in INDEX_SET_N)(tar[N[a,1],N[a,2]] >= 0);

constraint forall(a in INDEX_SET_N)(tea[N[a,1],N[a,2]] >= 0);

constraint forall(a in INDEX_SET_N)(tla[N[a,1],N[a,2]] >= 0);

constraint forall(a in INDEX_SET_N)(ted[N[a,1],N[a,2]] >= 0);

constraint forall(a in INDEX_SET_N)(tld[N[a,1],N[a,2]] >= 0);



solve minimize 5 * timePenalty + totalDistance / Maxspeed;




