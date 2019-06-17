enum I;

array[I] of float: a = array1d(I, [1 | i in I where not t[i] = true]);

array[I] of bool: t;




solve satisfy;


