include "var_perm_sym.mzn";

predicate var_sqr_sym(array[int, int] of var int: x) =
	let {int: n = card(index_set_1of2(x)); int: n2 = card(index_set_2of2(x)); int: l = n * n; constraint forall(i in 1..8, j in 1..l)(assert(n = n2,"square symmetry applied to non-square array")); array[1..l] of var int: y = [x[i,j] | i in index_set_1of2(x), j in index_set_2of2(x)]; array[1..8, 1..l] of 1..l: p = array2d(1..8,1..l,[if k = 1 then i * n + j - n elseif k = 2 then (n - j) * n + i elseif k = 3 then (n - i) * n + (n - j) + 1 elseif k = 4 then (j * n - n) + (n - i + 1) elseif k = 5 then (n - i) * n + j elseif k = 6 then (i * n - n) + (n - j + 1) elseif k = 7 then (n - j) * n + (n - i + 1) else (j * n - n) + i endif | k in 1..8, i,j in 1..n])} in
	var_perm_sym(y,p);

solve satisfy;


