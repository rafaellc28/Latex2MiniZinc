enum I;

array[I] of float: a;

float: BigM = 1 + sum(i in I)(abs(a[i]));

array[I] of float: r = array1d(I, [1 + sum(j in I)(if (a[j] < a[i] \/ a[j] = a[i] /\ j < i) then 1 else 0 endif) | i in I]);

array[I] of float: s = array1d(I, [1 + sum(j in I where a[i] < a[j] \/ a[i] = a[j] /\ i < j)(1) | i in I]);


array[I, I] of var bool: y;

array[I] of var float: t;


constraint forall(i in I, j in I where i != j)(a[i] <= a[j] + BigM * y[i,j]);

constraint forall(i in I, j in I where i != j)(a[j] <= a[i] + BigM * (1 - y[i,j]));

constraint forall(i in I, j in I where i != j)(y[i,j] + y[j,i] = 1);

constraint forall(i in I)(t[i] = 1 + sum(j in I where i != j)(y[i,j]));

solve satisfy;


