array[INDEX_SET_compatible] of set of int: compatible;

set of int: POS = 1..n;

enum HORSE;

array[int] of int: speed;

array[int] of int: endur;

int: n;

array[int] of int: strength;

enum RIDER;


array[INDEX_SET_h_1] of var HORSE: h;

array[INDEX_SET_r_1] of var RIDER: r;

set of int: INDEX_SET_compatible;

set of int: INDEX_SET_h_1;

set of int: INDEX_SET_r_1;


include "alldifferent.mzn";

constraint forall(i in 1..floor(n div 2 - 1))(speed[h[i]] < speed[h[i + 1]] /\ endur[r[i]] < endur[r[i + 1]]);

constraint forall(i in floor(n div 2)..floor(n - 1))(speed[h[i]] > speed[h[i + 1]] /\ endur[r[i]] > endur[r[i + 1]]);

constraint alldifferent(r);

constraint alldifferent(h);

constraint forall(p in POS)(r[p] in compatible[h[p]]);



solve maximize sum(p in POS)(strength[r[p]]);




