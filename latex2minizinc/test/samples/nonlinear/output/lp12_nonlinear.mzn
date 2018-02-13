set of int: I = 1..n;

float: b = 0.9;

float: a = 0.99;

int: n = 10;

array[int] of float: ub;

array[int] of float: lb;

array[int] of float: x0;


array[INDEX_SET_x_1] of var float: x;

var float: G1;

var float: G2;

var float: G5;

var float: G6;

set of int: INDEX_SET_x_1;


constraint forall(i in I)(x[i] <= ub[i] /\ x[i] >= lb[i]);

constraint G1 = 35.82 - 0.222 * x[10] - b * x[9];

constraint G2 = -133 + 3 * x[7] - a * x[10];

constraint G5 = 1.12 * x[1] + 0.13167 * x[1] * x[8] - 0.00667 * x[1] * pow(x[8],2) - a * x[4];

constraint G6 = 57.425 + 1.098 * x[8] - 0.038 * pow(x[8],2) + 0.325 * x[6] - a * x[7];

constraint G1 >= 0;

constraint G2 >= 0;

constraint -G1 + x[9] * (1 / b - b) >= 0;

constraint -G2 + (1 / a - a) * x[10] >= 0;

constraint G5 >= 0;

constraint G6 >= 0;

constraint -G5 + (1 / a - a) * x[4] >= 0;

constraint -G6 + (1 / a - a) * x[7] >= 0;

constraint 1.22 * x[4] - x[1] - x[5] = 0;

constraint 98000 * x[3] / (x[4] * x[9] + 1000 * x[3]) - x[6] = 0;

constraint (x[2] + x[5]) / x[1] - x[8] = 0;



var float: obj = 5.04 * x[1] + 0.035 * x[2] + 10 * x[3] + 3.36 * x[5] - 0.063 * x[4] * x[7];

solve minimize obj;




