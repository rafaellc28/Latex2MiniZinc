array[1..3] of var float: x;


constraint forall(i0 in 1..3)(x[i0] >= 0 /\ x[i0] <= 1);

constraint x[1] + x[2] + x[3] = 1;



solve minimize -32.174 * (255 * ln((x[1] + x[2] + x[3] + 0.03) / (0.09 * x[1] + x[2] + x[3] + 0.03)) + 280 * ln((x[2] + x[3] + 0.03) / (0.07 * x[2] + x[3] + 0.03)) + 290 * ln((x[3] + 0.03) / (0.13 * x[3] + 0.03)));




