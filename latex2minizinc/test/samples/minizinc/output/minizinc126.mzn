set of int: OBJ = 1..n;

int: n = 4;

array[OBJ] of int: size = [5,8,9,12];

array[OBJ] of int: value = [3,5,7,8];

int: limit = 29;


array[OBJ] of var int: x;


constraint forall(i in OBJ)(x[i] >= 0);

constraint sum(i in OBJ)(size[i] * x[i]) <= limit;



solve maximize sum(i in OBJ)(value[i] * x[i]);




