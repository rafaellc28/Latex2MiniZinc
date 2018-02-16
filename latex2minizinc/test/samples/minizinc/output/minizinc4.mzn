enum DISH;

array[int] of int: size;

int: capacity;

array[int] of int: satisf;


array[INDEX_SET_amt_1] of var int: amt;

set of int: INDEX_SET_amt_1;


constraint forall(i in DISH)(amt[i] >= 0);

constraint sum(i in DISH)(size[i] * amt[i]) <= capacity;



var float: obj = sum(i in DISH)(satisf[i] * amt[i]);

solve maximize obj;




