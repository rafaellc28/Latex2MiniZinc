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


array[I] of var float: x;


constraint assert(a >= 0, "Assertion a >= 0 failed!");

constraint assert(b >= 0, "Assertion b >= 0 failed!");

constraint assert(c >= 0, "Assertion c >= 0 failed!");

constraint assert(d >= 0, "Assertion d >= 0 failed!");

constraint assert(e >= 0, "Assertion e >= 0 failed!");

constraint assert(f >= 0, "Assertion f >= 0 failed!");

constraint assert(g >= 0, "Assertion g >= 0 failed!");

constraint assert(h >= 0, "Assertion h >= 0 failed!");

constraint 1 - a * (x[4] + x[6]) >= 0;

constraint 1 - a * (x[5] + x[7] - x[4]) >= 0;

constraint 1 - b * (x[8] - x[5]) >= 0;

constraint x[1] * x[6] - c * x[4] - d * x[1] + e >= 0;

constraint x[2] * x[7] - f * x[5] - x[2] * x[4] + f * x[4] >= 0;

constraint x[3] * x[8] - g - x[3] * x[5] + h * x[5] >= 0;

constraint x[1] <= 10000 /\ x[1] >= 100;

constraint forall(i in {2,3})(x[i] <= 10000 /\ x[i] >= 1000);

constraint forall(i in 4..8)(x[i] <= 1000 /\ x[i] >= 10);



solve minimize x[1] + x[2] + x[3];




