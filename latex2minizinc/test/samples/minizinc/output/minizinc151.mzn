enum MONKEY;

set of int: POS = 1..n;

int: n = card(MONKEY);

array[MONKEY, MONKEY] of int: coop;


array[POS] of var MONKEY: monkey;


include "alldifferent.mzn";

constraint alldifferent(monkey);



solve maximize sum(i in 1..floor(n - 1))(coop[monkey[i],monkey[i + 1]]);




