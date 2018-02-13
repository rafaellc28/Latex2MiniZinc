set of int: I = 1..N;

float: a;

float: b;

float: c;

float: d;

float: e;

float: f;

int: N = 13;


array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_x_1;


constraint forall(i in I)(x[i] >= 0);

constraint x[3] - x[2] >= 0;

constraint x[2] - x[1] >= 0;

constraint 1 - a * x[7] + a * x[8] >= 0;

constraint x[11] + x[12] + x[13] >= 50;

constraint x[13] - b * x[10] + c * x[3] * x[10] >= 0;

constraint x[5] - d * x[2] - e * x[2] * x[5] + f * pow(x[2],2) >= 0;

constraint x[6] - d * x[3] - e * x[3] * x[6] + f * pow(x[3],2) >= 0;

constraint x[4] - d * x[1] - e * x[1] * x[4] + f * pow(x[1],2) >= 0;

constraint x[12] - b * x[9] + c * x[2] * x[9] >= 0;

constraint x[11] - b * x[8] + c * x[1] * x[8] >= 0;

constraint x[5] * x[7] - x[1] * x[8] - x[4] * x[7] + x[4] * x[8] >= 0;

constraint 1 - a * (x[2] * x[9] + x[5] * x[8] - x[1] * x[8] - x[6] * x[9]) - x[5] - x[6] >= 0;

constraint x[2] * x[9] - x[3] * x[10] - x[6] * x[9] - 500 * x[2] + 500 * x[6] + x[2] * x[10] >= 0;

constraint x[2] - 0.9 - a * (x[2] * x[10] - x[3] * x[10]) >= 0;

constraint x[11] + x[12] + x[13] <= 250;

constraint x[1] <= 1 /\ x[1] >= 0.1;

constraint x[2] <= 1 /\ x[2] >= 0.1;

constraint x[3] <= 1 /\ x[3] >= 0.1;

constraint x[4] <= 0.1 /\ x[4] >= 0.0001;

constraint x[5] <= 0.9 /\ x[5] >= 0.1;

constraint x[6] <= 0.9 /\ x[6] >= 0.1;

constraint x[7] <= 1000 /\ x[7] >= 0.1;

constraint x[8] <= 1000 /\ x[8] >= 0.1;

constraint x[9] <= 1000 /\ x[9] >= 500;

constraint x[10] <= 500 /\ x[10] >= 0.1;

constraint x[11] <= 150 /\ x[11] >= 1;

constraint x[12] <= 150 /\ x[12] >= 0.0001;

constraint x[13] <= 150 /\ x[13] >= 0.0001;



var float: obj = x[11] + x[12] + x[13];

solve minimize obj;




