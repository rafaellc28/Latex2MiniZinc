set of int: COURSE = 1..len;

set of int: TASTE = 1..6;

set of int: TEMP = 1..3;

set of int: DISH = 1..ndish;

array[int] of int: taste;

float: salty;

float: sweet;

float: spicy;

float: bland;

float: sour;

float: umame;

int: len;

array[int] of int: temp;

int: hot = 1;

int: c;

int: cold = 2;

int: warm = 3;

array[int] of bool: heavy;

array[int] of int: value;

int: ndish;


var int: obj = (sum(c in COURSE)(value[dish[c]])) + (len - 1) + sum(c in 1..floor(len - 1))((temp[dish[c]] != temp[dish[c + 1]]) + sum(c in 1..floor(len - 1))(heavy[dish[c]] != heavy[dish[c + 1]]));

array[INDEX_SET_dish_1] of var DISH: dish;

set of int: INDEX_SET_bland_sweet;

set of int: INDEX_SET_bland_umame;

set of int: INDEX_SET_dish_1 = COURSE;

set of int: INDEX_SET_spicy_sour_bland;

array[INDEX_SET_bland_sweet] of int: bland_sweet;

array[INDEX_SET_bland_umame] of int: bland_umame;

array[INDEX_SET_spicy_sour_bland] of int: spicy_sour_bland;


include "alldifferent.mzn";

constraint alldifferent(dish);

constraint taste[dish[1]] = salty;

constraint taste[dish[len]] = sweet;

constraint forall(c in 1..floor(len - 1))((taste[dish[c]] = spicy -> (taste[dish[c + 1]] in bland_sweet)) /\ (taste[dish[c]] = sour -> (taste[dish[c + 1]] in bland_umame)) /\ (taste[dish[c]] = sweet -> (taste[dish[c + 1]] in spicy_sour_bland)));

constraint forall(c in 1..floor(len - 1))(taste[dish[c]] != taste[dish[c + 1]]);

constraint temp[dish[c]] = hot -> forall(c1 in floor(c + 1)..len)((temp[dish[c1]] = cold -> exists(c2 in floor(c + 1)..floor(c1 - 1))((temp[dish[c2]] = warm))));

constraint forall(c in 1..floor(len - 2))(heavy[dish[c]] = true /\ heavy[dish[c + 1]] = true -> not heavy[dish[c + 2]] = true);



solve maximize obj;




