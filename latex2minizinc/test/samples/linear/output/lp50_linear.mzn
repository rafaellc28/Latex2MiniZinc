set of int: PATTERNS = 1..nPAT;

enum WIDTHS;

float: lambda = 0.85;

array[WIDTHS] of float: price;

array[WIDTHS] of float: orders;

float: roll_width;

int: nPAT;

array[WIDTHS, PATTERNS] of int: nbr;


array[PATTERNS] of var int: Cut;

array[WIDTHS] of var int: Use;


constraint forall(w in WIDTHS)(assert(orders[w] > 0, "Assertion orders[\(w)] > 0 failed!"));

constraint assert(nPAT >= 0, "Assertion nPAT >= 0 failed!");

constraint forall(w in WIDTHS, p in PATTERNS)(assert(nbr[w,p] >= 0, "Assertion nbr[\(w),\(p)] >= 0 failed!"));

constraint forall(p in PATTERNS)(Cut[p] >= 0);

constraint forall(w in WIDTHS)(Use[w] >= 0);

constraint forall(i in WIDTHS)(sum(j in PATTERNS)(nbr[i,j] * Cut[j]) >= orders[i]);

constraint sum(i in WIDTHS)(i * Use[i]) <= roll_width;



solve minimize lambda * (sum(j in PATTERNS)(Cut[j])) + (1 - lambda) * (1 - sum(i in WIDTHS)(price[i] * Use[i]));




