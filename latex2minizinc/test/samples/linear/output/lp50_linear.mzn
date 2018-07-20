set of int: PATTERNS = 1..nPAT;

enum WIDTHS;

float: lambda = 0.85;

array[int] of float: price;

array[int] of float: orders;

float: roll_width;

int: nPAT;

array[int, int] of int: nbr;


array[INDEX_SET_Cut_1] of var int: Cut;

array[INDEX_SET_Use_1] of var int: Use;

set of int: INDEX_SET_Cut_1 = PATTERNS;

set of int: INDEX_SET_Use_1 = WIDTHS;


constraint forall(w in WIDTHS)(assert(orders[w] > 0, "Assertion orders[\(w)] > 0 failed!"));

constraint assert(nPAT >= 0, "Assertion nPAT >= 0 failed!");

constraint forall(w in WIDTHS, p in PATTERNS)(assert(nbr[w,p] >= 0, "Assertion nbr[\(w),\(p)] >= 0 failed!"));

constraint forall(p in INDEX_SET_Cut_1)(Cut[p] >= 0);

constraint forall(w in INDEX_SET_Use_1)(Use[w] >= 0);

constraint forall(i in WIDTHS)(sum(j in PATTERNS)(nbr[i,j] * Cut[j]) >= orders[i]);

constraint sum(i in WIDTHS)(i * Use[i]) <= roll_width;



solve minimize lambda * (sum(j in PATTERNS)(Cut[j])) + (1 - lambda) * (1 - sum(i in WIDTHS)(price[i] * Use[i]));




