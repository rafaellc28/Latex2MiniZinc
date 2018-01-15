int: M;

int: P;


array[INDEX_SET_x_1] of var int: x;

set of int: INDEX_SET_x_1 = M..9;


constraint forall(i in INDEX_SET_x_1)(x[i] >= 0);

constraint forall(i in 2..5)(x[i] + x[i + 1] <= 80);

constraint forall(i in M..9 where (i-M) mod P = 0)(x[i] + x[i + 1] <= 100);



var float: obj = 3 * x[1] + 2 * x[10];

solve maximize obj;




