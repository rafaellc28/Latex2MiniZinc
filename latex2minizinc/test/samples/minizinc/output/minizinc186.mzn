set of int: COURSE = 1..len;

set of int: TASTE = 1..6;

set of int: TEMP = 1..3;

set of int: DISH = 1..ndish;

array[DISH] of int: taste;

int: salty = 3;

int: sweet = 4;

int: spicy = 1;

int: bland = 6;

int: sour = 2;

int: umame = 5;

int: len;

array[DISH] of int: temp;

int: hot = 1;

int: c;

int: cold = 2;

int: warm = 3;

array[DISH] of bool: heavy;

array[DISH] of int: value;

int: ndish;


var int: obj = (sum(c in COURSE)(value[dish[c]])) + (len - 1) + sum(c in 1..floor(len - 1))((temp[dish[c]] != temp[dish[c + 1]]) + sum(c in 1..floor(len - 1))(heavy[dish[c]] != heavy[dish[c + 1]]));

array[COURSE] of var DISH: dish;


include "alldifferent.mzn";

constraint alldifferent(dish);

constraint taste[dish[1]] = salty;

constraint taste[dish[len]] = sweet;

constraint forall(c in 1..floor(len - 1))((taste[dish[c]] = spicy -> (taste[dish[c + 1]] in {bland,sweet})) /\ (taste[dish[c]] = sour -> (taste[dish[c + 1]] in {bland,umame})) /\ (taste[dish[c]] = sweet -> (taste[dish[c + 1]] in {spicy,sour,bland})));

constraint forall(c in 1..floor(len - 1))(taste[dish[c]] != taste[dish[c + 1]]);

constraint temp[dish[c]] = hot -> forall(c1 in floor(c + 1)..len)((temp[dish[c1]] = cold -> exists(c2 in floor(c + 1)..floor(c1 - 1))((temp[dish[c2]] = warm))));

constraint forall(c in 1..floor(len - 2))(heavy[dish[c]] = true /\ heavy[dish[c + 1]] = true -> not heavy[dish[c + 2]] = true);



solve maximize obj;




