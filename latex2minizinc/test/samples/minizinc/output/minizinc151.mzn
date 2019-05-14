enum MONKEY;

set of int: POS = 1..n;

int: n = card(MONKEY);

array[int, int] of int: coop;


array[INDEX_SET_monkey_1] of var MONKEY: monkey;

set of int: INDEX_SET_monkey_1 = POS;


include "alldifferent.mzn";

constraint alldifferent(monkey);



solve maximize sum(i in 1..floor(n - 1))(coop[monkey[i],monkey[i + 1]]);




