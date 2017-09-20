set of int: P = [PLANES[p,1]| p in INDEX_SET_PLANES];

array[INDEX_SET_N, 1..2] of LOCATIONS: N = CUSTOMERS_union_START_union_FINISH;

array[INDEX_SET_START, 1..2] of int: START = array2d(INDEX_SET_START, 1..2, [if idx2 == 1 then PLANES[p,1] else PLANES[p,2] endif | p in INDEX_SET_PLANES, idx2 in 1..2]);

array[INDEX_SET_FINISH, 1..2] of int: FINISH = array2d(INDEX_SET_FINISH, 1..2, [if idx2 == 1 then PLANES[p,1] else PLANES[p,3] endif | p in INDEX_SET_PLANES, idx2 in 1..2]);

array[INDEX_SET_CUSTOMERS, 1..2] of int: CUSTOMERS;

array[INDEX_SET_PLANES, 1..3] of int: PLANES;

enum LOCATIONS;

float: maxspeed;

array[INDEX_SET_gcdist_1, INDEX_SET_gcdist_2] of float: gcdist = array2d(INDEX_SET_gcdist_1, INDEX_SET_gcdist_2, [2 * 6371 * atan(sqrt(alpha[a,b])/sqrt(1 - alpha[a,b])) | a in LOCATIONS, b in LOCATIONS]);

float: bigM = 50;

float: minspeed;

array[int, int] of float: T1;

array[INDEX_SET_TF1_1, INDEX_SET_TF1_2] of float: TF1 = array2d(INDEX_SET_TF1_1, INDEX_SET_TF1_2, [max(q in INDEX_SET_PLANES where (FINISH[p,1] = PLANES[q,1]) /\ (FINISH[p,2] = PLANES[q,3]))(F1[FINISH[p,1],PLANES[q,2],FINISH[p,2]]) | p in INDEX_SET_FINISH]);

array[int, int] of float: T2;

array[INDEX_SET_TF2_1, INDEX_SET_TF2_2] of float: TF2 = array2d(INDEX_SET_TF2_1, INDEX_SET_TF2_2, [min(q in INDEX_SET_PLANES where (FINISH[p,1] = PLANES[q,1]) /\ (FINISH[p,2] = PLANES[q,3]))(F2[FINISH[p,1],PLANES[q,2],FINISH[p,2]]) | p in INDEX_SET_FINISH]);

array[INDEX_SET_TS1_1, INDEX_SET_TS1_2] of float: TS1 = array2d(INDEX_SET_TS1_1, INDEX_SET_TS1_2, [max(q in INDEX_SET_PLANES where (START[p,1] = PLANES[q,1]) /\ (START[p,2] = PLANES[q,2]))(S1[START[p,1],START[p,2],PLANES[q,3]]) | p in INDEX_SET_START]);

array[INDEX_SET_TS2_1, INDEX_SET_TS2_2] of float: TS2 = array2d(INDEX_SET_TS2_1, INDEX_SET_TS2_2, [min(q in INDEX_SET_PLANES where (START[p,1] = PLANES[q,1]) /\ (START[p,2] = PLANES[q,2]))(S2[START[p,1],START[p,2],PLANES[q,3]]) | p in INDEX_SET_START]);

array[int, int, int] of float: S2;

array[int, int, int] of float: F2;

array[int] of float: lat;

array[int] of float: lng;

float: d2r = 3.1415926 / 180;

array[int, int, int] of float: S1;

array[int, int, int] of float: F1;

array[INDEX_SET_alpha_1, INDEX_SET_alpha_2] of float: alpha = array2d(INDEX_SET_alpha_1, INDEX_SET_alpha_2, [pow(sin(d2r * (lat[a] - lat[b]) / 2),2) + cos(d2r * lat[a]) * cos(d2r * lat[b]) * pow(sin(d2r * (lng[a] - lng[b]) / 2),2) | a in LOCATIONS, b in LOCATIONS]);


var float: timePenalty;

var float: totalDistance;

array[INDEX_SET_routeDistance_1] of var float: routeDistance;

array[INDEX_SET_y_1, INDEX_SET_y_2, INDEX_SET_y_3, INDEX_SET_y_4, INDEX_SET_y_5] of var float: y;

array[INDEX_SET_tlv_1, INDEX_SET_tlv_2] of var float: tlv;

array[INDEX_SET_tar_1, INDEX_SET_tar_2] of var float: tar;

array[INDEX_SET_tea_1, INDEX_SET_tea_2] of var float: tea;

array[INDEX_SET_tla_1, INDEX_SET_tla_2] of var float: tla;

array[INDEX_SET_ted_1, INDEX_SET_ted_2] of var float: ted;

array[INDEX_SET_tld_1, INDEX_SET_tld_2] of var float: tld;

array[INDEX_SET_x_1, INDEX_SET_x_2, INDEX_SET_x_3, INDEX_SET_x_4, INDEX_SET_x_5] of var bool: x;

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

set of int: INDEX_SET_TF1_1;

set of int: INDEX_SET_TF1_2;

set of int: INDEX_SET_TF2_1;

set of int: INDEX_SET_TF2_2;

set of int: INDEX_SET_TS1_1;

set of int: INDEX_SET_TS1_2;

set of int: INDEX_SET_TS2_1;

set of int: INDEX_SET_TS2_2;

set of int: INDEX_SET_alpha_1;

set of int: INDEX_SET_alpha_2;

set of int: INDEX_SET_gcdist_1;

set of int: INDEX_SET_gcdist_2;

set of int: INDEX_SET_routeDistance_1;

set of int: INDEX_SET_tar_1;

set of int: INDEX_SET_tar_2;

set of int: INDEX_SET_tea_1;

set of int: INDEX_SET_tea_2;

set of int: INDEX_SET_ted_1;

set of int: INDEX_SET_ted_2;

set of int: INDEX_SET_tla_1;

set of int: INDEX_SET_tla_2;

set of int: INDEX_SET_tld_1;

set of int: INDEX_SET_tld_2;

set of int: INDEX_SET_tlv_1;

set of int: INDEX_SET_tlv_2;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;

set of int: INDEX_SET_x_3;

set of int: INDEX_SET_x_4;

set of int: INDEX_SET_x_5;

set of int: INDEX_SET_y_1;

set of int: INDEX_SET_y_2;

set of int: INDEX_SET_y_3;

set of int: INDEX_SET_y_4;

set of int: INDEX_SET_y_5;

array[INDEX_SET_START_union_CUSTOMERS,1..2] of int: START_union_CUSTOMERS;


constraint timePenalty >= 0;

constraint totalDistance >= 0;

constraint forall(p in P)(routeDistance[p] >= 0);

constraint forall(p in P, a in INDEX_SET_N, b in INDEX_SET_N)(y[p,N[a,1],N[a,2],N[b,1],N[b,2]] >= 0);

constraint forall(a in INDEX_SET_N)(tea[N[a,1],N[a,2]] >= 0);

constraint forall(a in INDEX_SET_N)(tla[N[a,1],N[a,2]] >= 0);

constraint forall(a in INDEX_SET_N)(ted[N[a,1],N[a,2]] >= 0);

constraint forall(a in INDEX_SET_N)(tld[N[a,1],N[a,2]] >= 0);

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

constraint forall(p in P, a in INDEX_SET_N, b in INDEX_SET_N)(tar[N[b,1],N[b,2]] >= tlv[N[a,1],N[a,2]] + gcdist[N[a,2],N[b,2]] / maxspeed - bigM * (1 - x[p,N[a,1],N[a,2],N[b,1],N[b,2]]));

constraint forall(p in P, a in INDEX_SET_N, b in INDEX_SET_N)(tar[N[b,1],N[b,2]] <= tlv[N[a,1],N[a,2]] + gcdist[N[a,2],N[b,2]] / minspeed + bigM * (1 - x[p,N[a,1],N[a,2],N[b,1],N[b,2]]));

constraint forall(a in INDEX_SET_CUSTOMERS)(tea[CUSTOMERS[a,1],CUSTOMERS[a,2]] >= T1[CUSTOMERS[a,1],CUSTOMERS[a,2]] - tar[CUSTOMERS[a,1],CUSTOMERS[a,2]]);

constraint forall(a in INDEX_SET_FINISH)(tea[FINISH[a,1],FINISH[a,2]] >= TF1[FINISH[a,1],FINISH[a,2]] - tar[FINISH[a,1],FINISH[a,2]]);

constraint forall(a in INDEX_SET_CUSTOMERS)(tla[CUSTOMERS[a,1],CUSTOMERS[a,2]] >= tar[CUSTOMERS[a,1],CUSTOMERS[a,2]] - T2[CUSTOMERS[a,1],CUSTOMERS[a,2]]);

constraint forall(a in INDEX_SET_FINISH)(tla[FINISH[a,1],FINISH[a,2]] >= tar[FINISH[a,1],FINISH[a,2]] - TF2[FINISH[a,1],FINISH[a,2]]);

constraint forall(a in INDEX_SET_START)(ted[START[a,1],START[a,2]] >= TS1[START[a,1],START[a,2]] - tlv[START[a,1],START[a,2]]);

constraint forall(a in INDEX_SET_CUSTOMERS)(ted[CUSTOMERS[a,1],CUSTOMERS[a,2]] >= T1[CUSTOMERS[a,1],CUSTOMERS[a,2]] - tlv[CUSTOMERS[a,1],CUSTOMERS[a,2]]);

constraint forall(a in INDEX_SET_START)(tld[START[a,1],START[a,2]] >= tlv[START[a,1],START[a,2]] - TS2[START[a,1],START[a,2]]);

constraint forall(a in INDEX_SET_CUSTOMERS)(tld[CUSTOMERS[a,1],CUSTOMERS[a,2]] >= tlv[CUSTOMERS[a,1],CUSTOMERS[a,2]] - T2[CUSTOMERS[a,1],CUSTOMERS[a,2]]);

constraint forall(p in P)(routeDistance[p] = sum(a in INDEX_SET_N, b in INDEX_SET_N)(gcdist[N[a,2],N[b,2]] * x[p,N[a,1],N[a,2],N[b,1],N[b,2]]));

constraint totalDistance = sum(p in P)(routeDistance[p]);

constraint timePenalty = sum(a in INDEX_SET_N)((tea[N[a,1],N[a,2]] + 2 * tla[N[a,1],N[a,2]] + 2 * ted[N[a,1],N[a,2]] + tld[N[a,1],N[a,2]]));

constraint forall(p in P, a in INDEX_SET_N, b in INDEX_SET_N)(y[p,N[a,1],N[a,2],N[b,1],N[b,2]] <= card(INDEX_SET_CUSTOMERS) * x[p,N[a,1],N[a,2],N[b,1],N[b,2]]);



var float: obj = 5 * timePenalty + totalDistance / maxspeed;

solve minimize obj;




