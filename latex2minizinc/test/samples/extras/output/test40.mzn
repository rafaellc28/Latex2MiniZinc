enum I;

array[int] of float: D;


constraint forall(i in I where 1 = 1 /\ forall(j in 1..10)(D[j] > 0))(1 < 2);

solve satisfy;


