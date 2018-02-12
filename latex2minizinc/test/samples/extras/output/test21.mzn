bool: a;

float: b;

float: c;

float: d;

float: e;


constraint if a = true then b + c - floor(1 / 2 * d / e) mod 9 else 0 endif <= 5;

solve satisfy;


