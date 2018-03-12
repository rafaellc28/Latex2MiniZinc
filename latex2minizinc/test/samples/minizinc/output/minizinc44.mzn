enum NEGOTIATOR;

NEGOTIATOR: dummy;

int: l;

int: u;

array[int, int] of int: joint;

int: m;

array[int] of int: honor;


array[INDEX_SET_party_1] of var NEGOTIATOR: party;

var int: obj;

set of int: INDEX_SET_party_1 = 1..u;


constraint forall(i in 1..l)(party[i] > dummy);

constraint forall(i in 1..floor(u - 1))(party[i] >= party[i + 1] + (party[i + 1] != dummy));

constraint sum(i,j in 1..u where i < j)(joint[party[i],party[j]]) >= m;

constraint obj = (min(j in 1..u)((party[j] = dummy) * max(honor) + honor[party[j]]));



solve maximize obj;




