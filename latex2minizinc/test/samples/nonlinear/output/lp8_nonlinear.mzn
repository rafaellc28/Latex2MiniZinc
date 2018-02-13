set of int: I = 1..N;

float: a;

float: b;

float: c;

float: d;

float: e;

float: f;

float: g;

float: h;

int: N = 8;


array[INDEX_SET_x_1] of var float: x;

set of int: INDEX_SET_x_1;


constraint 1 - a * (x[4] + x[6]) >= 0;

constraint 1 - a * (x[5] + x[7] - x[4]) >= 0;

constraint 1 - b * (x[8] - x[5]) >= 0;

constraint x[1] * x[6] - c * x[4] - d * x[1] + e >= 0;

constraint x[2] * x[7] - f * x[5] - x[2] * x[4] + f * x[4] >= 0;

constraint x[3] * x[8] - g - x[3] * x[5] + h * x[5] >= 0;

constraint x[1] <= 10000 /\ x[1] >= 100;

constraint forall(i in {2,3})(x[i] <= 10000 /\ x[i] >= 1000);

constraint forall(i in 4..8)(x[i] <= 1000 /\ x[i] >= 10);



var float: obj = x[1] + x[2] + x[3];

solve minimize obj;




