enum I;

array[1..10] of float: D;


constraint forall(i in I where forall(j in 1..10)(D[j] > 0 /\ 1 = 1))(1 < 2);

solve satisfy;


