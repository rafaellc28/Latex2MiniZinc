set of int: VERTEX = 1..n;

set of int: POLYGON = 1..m;

set of int: RANK = 1..n;

set of int: PVERTEX = 1..floor(n * m);

enum TRIBUTE;

array[TRIBUTE] of int: rank = [floor((i - 1)) div m + 1 | i in 1..floor(n * m)];

int: m;

int: n;


var int: tcoins = sum(i in 1..floor(m - 1), j in VERTEX)(ncoins[i,j]);

array[POLYGON, VERTEX] of var TRIBUTE: tribute;

array[1..floor(m - 1), VERTEX] of var 0..floor(n - 1): ncoins;

array[1..length(TRIBUTE)] of var PVERTEX: position;


include "lex_lesseq.mzn";

include "all_different.mzn";

include "inverse.mzn";

constraint all_different(array1d(tribute));

constraint forall(i in 1..floor(m - 1))(forall(j in VERTEX)(ncoins[i,j] = abs(rank[tribute[i,j]] - rank[tribute[i + 1,j]])));

constraint forall(j in 1..floor(n - 1))(lex_lesseq([tribute[i,j] | i in POLYGON],[tribute[i,j + 1] | i in POLYGON]));

constraint forall(j in 1..floor(n - 1))(tribute[1,j] < tribute[1,j + 1]);

constraint tribute[1,1] < tribute[m,1];

constraint inverse(array1d(tribute),position);

constraint forall(i in RANK)(forall(j in floor(m * (i - 1) + 1)..floor(m * i - 1))(position[j] < position[j + 1]));



solve maximize tcoins;




