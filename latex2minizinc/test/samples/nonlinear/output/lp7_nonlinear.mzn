set of int: I = 1..235;

float: PI = 4 * atan(1);

array[int] of float: y;


array[INDEX_SET_x_1] of var float: x;

array[INDEX_SET_a_1] of var float: a;

array[INDEX_SET_b_1] of var float: b;

array[INDEX_SET_c_1] of var float: c;

set of int: INDEX_SET_a_1;

set of int: INDEX_SET_b_1;

set of int: INDEX_SET_c_1;

set of int: INDEX_SET_x_1 = 1..8;


constraint forall(i in I)(a[i] = x[1] / x[6] * exp(-pow((y[i] - x[3]),2) / (2 * pow(x[6],2))));

constraint forall(i in I)(b[i] = x[2] / x[7] * exp(-pow((y[i] - x[4]),2) / (2 * pow(x[7],2))));

constraint forall(i in I)(c[i] = (1 - x[2] - x[1]) / x[8] * exp(-pow((y[i] - x[5]),2) / (2 * pow(x[8],2))));

constraint 1 - x[1] - x[2] >= 0;

constraint forall(i in 1..2)(x[i] <= 0.499 /\ x[i] >= 0.001);

constraint x[3] <= 180 /\ x[3] >= 100;

constraint x[4] <= 210 /\ x[4] >= 130;

constraint x[5] <= 240 /\ x[5] >= 170;

constraint forall(i in 6..8)(x[i] <= 25 /\ x[i] >= 5);



var float: obj = -sum(i in I)(ln((a[i] + b[i] + c[i]) / sqrt(2 * PI)));

solve minimize obj;




