set of int: POTIONS = 1..n;

set of int: SEGMENTS = 1..m;

int: n;

int: w;

float: capacity;

int: p;

int: m;

array[POTIONS, SEGMENTS] of int: nutrient;

array[POTIONS, SEGMENTS] of int: leave;

array[POTIONS] of int: choice;


var int: total_nutrient = sum(nutrient_list);

var int: total_leaves = sum(leave_list);

array[POTIONS] of var int: nutrient_list = [nutrient[i,choice[i]] | i in POTIONS];

array[POTIONS] of var int: leave_list = [leave[i,choice[i]] | i in POTIONS];


constraint assert(n >= w,"Window Size larger than # of steps");

constraint total_nutrient <= capacity;

constraint forall(tail in w..n)(sum(i in floor(tail - w + 1)..tail)(leave_list[i]) >= p);



solve maximize total_leaves;




