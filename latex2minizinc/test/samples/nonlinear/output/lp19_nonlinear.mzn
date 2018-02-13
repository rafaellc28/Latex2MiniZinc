array[INDEX_SET_x_1] of var float: x;

var float: h;

set of int: INDEX_SET_x_1 = 1..6;


constraint h = (pow((x[1] - 1E+6),2) / 6.4E+13 + (x[1] - 1E+4) * (x[2] - 1) / 2E+4 + pow((x[2] - 1),2)) * pow((x[3] - 2E+6),2) / (0.96 * 4.9E+13) + pow((x[4] - 10),2) / 2.5E+3 + pow((x[5] - 1E-3),2) / 2.5E-3 + pow((x[6] - 1E+8),2) / 2.5E+17;

constraint x[1] + 4E+3 * x[2] - 1.76E+4 = 0;

constraint x[1] <= 2E+4 /\ x[1] >= 0;

constraint x[2] <= 10 /\ x[2] >= -10;

constraint x[3] <= 1E+7 /\ x[3] >= 0;

constraint x[4] <= 20 /\ x[4] >= 0;

constraint x[5] <= 1 /\ x[5] >= -1;

constraint x[6] <= 2E+8 /\ x[6] >= 0;



var float: obj = -exp(-h / 2);

solve minimize obj;




