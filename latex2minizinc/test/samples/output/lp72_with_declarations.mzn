set of int: I = 1..12;

array[I] of float: a = array1d(I, [Uniform(2,7) | i in I]);

array[I] of float: pos;

array[1..card(I)] of float: ind = array1d(1..card(I), [sum(i in I where pos[i] = k)(i) | k in 1..card(I)]);




solve satisfy;


