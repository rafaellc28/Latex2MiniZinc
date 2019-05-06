set of int: POTIONS = 1..n;

set of int: SEGMENTS = 1..m;

int: n;

int: w;

float: capacity;

int: p;

int: m;

array[int, int] of int: nutrient;

array[int, int] of int: leave;

array[int] of int: choice;


var int: total_nutrient = sum(nutrient_list);

var int: total_leaves = sum(leave_list);

array[INDEX_SET_nutrient_list_1] of var int: nutrient_list = [nutrient[i,choice[i]] | i in POTIONS];

array[INDEX_SET_leave_list_1] of var int: leave_list = [leave[i,choice[i]] | i in POTIONS];

set of int: INDEX_SET_leave_list_1 = POTIONS;

set of int: INDEX_SET_nutrient_list_1 = POTIONS;


constraint assert(n >= w,"Window Size larger than # of steps");

constraint total_nutrient <= capacity;

constraint forall(tail in w..n)(sum(i in floor(tail - w + 1)..tail)(leave_list[i]) >= p);



solve maximize total_leaves;




