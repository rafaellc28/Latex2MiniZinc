set of int: HOUR = 1..n;

set of int: HOUR0 = 0..n;

enum CHOICE = {heat,strongly_heat,cool,strongly_cool,do_nothing};

int: start;

array[int] of int: readings;

array[int] of int: effect = [1,4,-2,-5,0];

array[int] of int: cost = [1,5,3,9,0];

int: n = length(readings);


array[INDEX_SET_temp_1] of var 25..30: temp;

array[INDEX_SET_choice_1] of var CHOICE: choice;

var int: obj;

set of int: INDEX_SET_choice_1 = HOUR;

set of int: INDEX_SET_temp_1 = HOUR0;


constraint temp[0] = start;

constraint forall(h in HOUR)(temp[h] = (temp[h - 1] + readings[h]) div 2 + effect[choice[h]]);

constraint obj = sum(h in HOUR)(cost[choice[h]]);



solve minimize obj;




