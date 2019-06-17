enum PLACES;

PLACES: finish;

PLACES: start;

array[PLACES, PLACES] of float: gcdist = array2d(PLACES, PLACES, [2 * 6371 * atan(sqrt(alpha[a,b])/sqrt(1 - alpha[a,b])) | a in PLACES, b in PLACES]);

float: maxspeed;

float: bigM = 50;

array[PLACES] of float: S1;

array[PLACES] of float: S2;

array[PLACES] of float: lat;

array[PLACES] of float: lng;

float: d2r = 3.1415926 / 180;

array[PLACES, PLACES] of float: alpha = array2d(PLACES, PLACES, [pow(sin(d2r * (lat[a] - lat[b]) / 2),2) + cos(d2r * lat[a]) * cos(d2r * lat[b]) * pow(sin(d2r * (lng[a] - lng[b]) / 2),2) | a in PLACES, b in PLACES]);


array[PLACES] of var float: tea;

array[PLACES] of var float: tla;

array[PLACES] of var float: ted;

array[PLACES] of var float: tld;

var float: Tmax;

array[PLACES, PLACES] of var int: y;

array[PLACES] of var float: tlv;

array[PLACES] of var float: tar;

array[PLACES, PLACES] of var bool: x;


constraint assert(finish != start, "Assertion finish != start failed!");

constraint forall(p in PLACES)(assert(S2[p] >= S1[p], "Assertion S2[\(p)] >= S1[\(p)] failed!"));

constraint forall(a in PLACES)(tea[a] >= 0);

constraint forall(a in PLACES)(tla[a] >= 0);

constraint forall(a in PLACES)(ted[a] >= 0);

constraint forall(a in PLACES)(tld[a] >= 0);

constraint Tmax >= 0;

constraint forall(a in PLACES, b in PLACES)(y[a,b] >= 0);

constraint forall(a in PLACES where a != finish)(sum(b in PLACES)(x[a,b]) = 1);

constraint sum(b in PLACES)(x[finish,b]) = 0;

constraint forall(a in PLACES where a != start)(sum(b in PLACES)(x[b,a]) = 1);

constraint sum(b in PLACES)(x[b,start]) = 0;

constraint forall(a in PLACES, b in PLACES)(y[a,b] <= (card(PLACES) - 1) * x[a,b]);

constraint forall(a in PLACES)(sum(b in PLACES)(y[b,a] + (if a = start then card(PLACES) else 0 endif)) = 1 + sum(b in PLACES)(y[a,b]));

constraint forall(a in PLACES)(tlv[a] >= tar[a]);

constraint forall(a in PLACES, b in PLACES)(tar[b] >= tlv[a] + gcdist[a,b] / maxspeed - bigM * (1 - x[a,b]));

constraint forall(a in PLACES where a != start)(tea[a] >= S1[a] - tar[a]);

constraint forall(a in PLACES where a != start)(tla[a] >= tar[a] - S2[a]);

constraint forall(a in PLACES where a != finish)(ted[a] >= S1[a] - tlv[a]);

constraint forall(a in PLACES where a != finish)(tld[a] >= tlv[a] - S2[a]);

constraint forall(a in PLACES)(tea[a] <= Tmax);

constraint forall(a in PLACES)(tla[a] <= Tmax);

constraint forall(a in PLACES)(ted[a] <= Tmax);

constraint forall(a in PLACES)(tld[a] <= Tmax);



solve minimize sum(a in PLACES)((1 * tea[a] + 2 * tla[a] + 2 * ted[a] + 1 * tld[a]) + 2 * Tmax);




