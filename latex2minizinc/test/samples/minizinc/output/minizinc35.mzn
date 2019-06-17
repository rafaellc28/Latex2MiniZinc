set of int: VERTEX = 1..n;

set of int: RANK = 1..n;

set of int: POLYGON = 1..m;

enum TRIBUTE;

array[TRIBUTE] of int: rank = [floor((i - 1)) div m + 1 | i in 1..floor(n * m)];

int: m;

int: n;


var int: tcoins = sum(i in 1..floor(m - 1), j in VERTEX)(ncoins[i,j]);

array[POLYGON, VERTEX] of var TRIBUTE: tribute;

array[1..floor(m - 1), VERTEX] of var 0..floor(n - 1): ncoins;


include "all_different.mzn";

include "value_precede_chain.mzn";

constraint all_different(array1d(tribute));

constraint forall(i in 1..floor(m - 1))(forall(j in VERTEX)(ncoins[i,j] = abs(rank[tribute[i,j]] - rank[tribute[i + 1,j]])));

constraint forall(j in 1..floor(n - 1))(tribute[1,j] < tribute[1,j + 1]);

constraint tribute[1,1] < tribute[m,1];

constraint forall(r in RANK)(value_precede_chain([i | i in floor((r - 1) * m + 1)..floor(r * m)],array1d(tribute)));



solve maximize tcoins;




