array[INDEX_SET_compatible] of set of int: compatible;

set of int: POS = 1..n;

enum RIDER;

enum HORSE;

array[HORSE] of int: speed;

array[RIDER] of int: endur;

int: n;

array[RIDER] of int: strength;


array[POS] of var HORSE: h;

array[POS] of var RIDER: r;

set of int: INDEX_SET_compatible;


include "alldifferent.mzn";

constraint forall(i in 1..floor(n div 2 - 1))(speed[h[i]] < speed[h[i + 1]] /\ endur[r[i]] < endur[r[i + 1]]);

constraint forall(i in floor(n div 2)..floor(n - 1))(speed[h[i]] > speed[h[i + 1]] /\ endur[r[i]] > endur[r[i + 1]]);

constraint alldifferent(r);

constraint alldifferent(h);

constraint forall(p in POS)(r[p] in compatible[h[p]]);



solve maximize sum(p in POS)(strength[r[p]]);




