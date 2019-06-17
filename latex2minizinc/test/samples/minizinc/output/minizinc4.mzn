enum DISH;

enum TEST;

array[DISH] of int: size;

int: capacity;

array[DISH] of int: satisf;


array[DISH] of var int: amt;


constraint forall(i in DISH)(amt[i] >= 0);

constraint sum(i in DISH)(size[i] * amt[i]) <= capacity;



solve maximize sum(i in DISH)(satisf[i] * amt[i]);




