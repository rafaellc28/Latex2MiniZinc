enum NEGOTIATOR;

NEGOTIATOR: dummy;

int: l;

int: u;

array[NEGOTIATOR, NEGOTIATOR] of int: joint;

int: m;

array[NEGOTIATOR] of int: honor;


array[1..u] of var NEGOTIATOR: party;

var int: obj;


constraint forall(i in 1..l)(party[i] > dummy);

constraint forall(i in 1..floor(u - 1))(party[i] >= party[i + 1] + (party[i + 1] != dummy));

constraint sum(i,j in 1..u where i < j)(joint[party[i],party[j]]) >= m;

constraint obj = (min(j in 1..u)((party[j] = dummy) * max(honor) + honor[party[j]]));



solve maximize obj;




