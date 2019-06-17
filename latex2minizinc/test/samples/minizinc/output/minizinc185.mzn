set of int: COURSE = 1..len;

enum TASTE = {spicy,sour,salty,sweet,umame,bland};

enum TEMP = {hot,cold,warm};

enum DISH;

array[DISH] of TASTE: taste;

array[1..7, TASTE] of DISH: d;

array[DISH] of TEMP: temp;

array[1..3, TEMP] of int: e;

array[DISH] of bool: heavy;

int: len;

array[DISH] of int: value;


var int: obj = (sum(c in COURSE)(value[dish[c]])) + (len - 1) + sum(c in 1..floor(len - 1))((temp[dish[c]] != temp[dish[c + 1]]) + sum(c in 1..floor(len - 1))(heavy[dish[c]] != heavy[dish[c + 1]]));

array[COURSE] of var DISH: dish;


include "alldifferent.mzn";

include "regular.mzn";

constraint alldifferent(dish);

constraint regular([taste[dish[c]] | c in COURSE],7,card(TASTE),d,1,{5});

constraint regular([temp[dish[c]] | c in COURSE],3,card(TEMP),e,2,1..3);

constraint forall(c in 1..floor(len - 2))(heavy[dish[c]] = true /\ heavy[dish[c + 1]] = true -> not heavy[dish[c + 2]] = true);

constraint forall(i in 1..7, t in TASTE)(d[i,to_enum(TASTE,t)] in 0..7);

constraint forall(i in 1..3, t in TEMP)(e[i,to_enum(TEMP,t)] in 0..3);



solve maximize obj;




