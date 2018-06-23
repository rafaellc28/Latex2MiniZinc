enum PLACES;

PLACES: Finish;

PLACES: Start;

array[int, int] of float: Gcdist;

float: Maxspeed;

float: BigM;

array[int] of float: S1;

array[int] of float: S2;


array[INDEX_SET_tea_1] of var float: tea;

array[INDEX_SET_tla_1] of var float: tla;

array[INDEX_SET_ted_1] of var float: ted;

array[INDEX_SET_tld_1] of var float: tld;

var float: Tmax;

array[INDEX_SET_y_1, INDEX_SET_y_2] of var int: y;

array[INDEX_SET_tlv_1] of var float: tlv;

array[INDEX_SET_tar_1] of var float: tar;

array[INDEX_SET_x_1, INDEX_SET_x_2] of var bool: x;

set of int: INDEX_SET_tar_1 = PLACES;

set of int: INDEX_SET_tea_1 = PLACES;

set of int: INDEX_SET_ted_1 = PLACES;

set of int: INDEX_SET_tla_1 = PLACES;

set of int: INDEX_SET_tld_1 = PLACES;

set of int: INDEX_SET_tlv_1 = PLACES;

set of int: INDEX_SET_x_1 = PLACES;

set of int: INDEX_SET_x_2 = PLACES;

set of int: INDEX_SET_y_1 = PLACES;

set of int: INDEX_SET_y_2 = PLACES;


constraint forall(a in INDEX_SET_tea_1)(tea[a] >= 0);

constraint forall(a in INDEX_SET_tla_1)(tla[a] >= 0);

constraint forall(a in INDEX_SET_ted_1)(ted[a] >= 0);

constraint forall(a in INDEX_SET_tld_1)(tld[a] >= 0);

constraint Tmax >= 0;

constraint forall(a in INDEX_SET_y_1, b in INDEX_SET_y_2)(y[a,b] >= 0);

constraint forall(a in PLACES where a != Finish)(sum(b in PLACES)(x[a,b]) = 1);

constraint sum(b in PLACES)(x[Finish,b]) = 0;

constraint forall(a in PLACES where a != Start)(sum(b in PLACES)(x[b,a]) = 1);

constraint sum(b in PLACES)(x[b,Start]) = 0;

constraint forall(a in PLACES, b in PLACES)(y[a,b] <= (card(PLACES) - 1) * x[a,b]);

constraint forall(a in PLACES)(sum(b in PLACES)(y[b,a] + (if a = Start then card(PLACES) else 0 endif)) = 1 + sum(b in PLACES)(y[a,b]));

constraint forall(a in PLACES)(tlv[a] >= tar[a]);

constraint forall(a in PLACES, b in PLACES)(tar[b] >= tlv[a] + Gcdist[a,b] / Maxspeed - BigM * (1 - x[a,b]));

constraint forall(a in PLACES where a != Start)(tea[a] >= S1[a] - tar[a]);

constraint forall(a in PLACES where a != Start)(tla[a] >= tar[a] - S2[a]);

constraint forall(a in PLACES where a != Finish)(ted[a] >= S1[a] - tlv[a]);

constraint forall(a in PLACES where a != Finish)(tld[a] >= tlv[a] - S2[a]);

constraint forall(a in PLACES)(tea[a] <= Tmax);

constraint forall(a in PLACES)(tla[a] <= Tmax);

constraint forall(a in PLACES)(ted[a] <= Tmax);

constraint forall(a in PLACES)(tld[a] <= Tmax);



solve minimize sum(a in PLACES)((1 * tea[a] + 2 * tla[a] + 2 * ted[a] + 1 * tld[a]) + 2 * Tmax);




