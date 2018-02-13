float: b = sin(b1);

float: a;

float: c = cos(b1);

float: b1;


array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_x_1 = 1..9;


constraint x[4] - x[3] + 0.55 >= 0;

constraint x[3] - x[4] + 0.55 >= 0;

constraint 2250000 - pow(x[1],2) - pow(x[8],2) >= 0;

constraint 2250000 - pow(x[2],2) - pow(x[9],2) >= 0;

constraint x[5] * x[6] * sin(-x[3] - 0.25) + x[5] * x[7] * sin(-x[4] - 0.25) + 2 * b * pow(x[5],2) - a * x[1] + 400 * a = 0;

constraint x[5] * x[6] * sin(x[3] - 0.25) + x[6] * x[7] * sin(x[3] - x[4] - 0.25) + 2 * b * pow(x[6],2) - a * x[2] + 400 * a = 0;

constraint x[5] * x[7] * sin(x[4] - 0.25) + x[6] * x[7] * sin(x[4] - x[3] - 0.25) + 2 * b * pow(x[7],2) + 881.779 * a = 0;

constraint a * x[8] + x[5] * x[6] * cos(-x[3] - 0.25) + x[5] * x[7] * cos(-x[4] - 0.25) - 200 * a - 2 * c * pow(x[5],2) + 0.7533E-3 * a * pow(x[5],2) = 0;

constraint a * x[9] + x[5] * x[6] * cos(x[3] - 0.25) + x[6] * x[7] * cos(x[3] - x[4] - 0.25) - 2 * c * pow(x[6],2) + 0.7533E-3 * a * pow(x[6],2) - 200 * a = 0;

constraint x[5] * x[7] * cos(x[4] - 0.25) + x[6] * x[7] * cos(x[4] - x[3] - 0.25) - 2 * c * pow(x[7],2) + 22.938 * a + 0.7533E-3 * a * pow(x[7],2) = 0;

constraint forall(i in 1..2)(x[i] >= 0);

constraint forall(i in 3..4)(x[i] <= 0.55 /\ x[i] >= -0.55);

constraint forall(i in 5..7)(x[i] <= 252 /\ x[i] >= 196);

constraint forall(i in 8..9)(x[i] <= 800 /\ x[i] >= -400);



var float: obj = 3 * x[1] + 1E-6 * pow(x[1],3) + 2 * x[2] + 0.522074E-6 * pow(x[2],3);

solve minimize obj;




