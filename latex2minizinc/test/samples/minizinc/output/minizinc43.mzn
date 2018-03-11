enum NEGOTIATOR;

int: l;

int: u;

NEGOTIATOR: dummy;

array[int, int] of int: joint;

int: m;

array[int] of int: honor;


var set of NEGOTIATOR: party;

var int: obj;


constraint card(party) >= l /\ card(party) <= u;

constraint not (dummy in party);

constraint sum(i,j in party where i < j)(joint[i,j]) >= m;

constraint obj = (min(j in party)(honor[j]));



solve maximize obj;




