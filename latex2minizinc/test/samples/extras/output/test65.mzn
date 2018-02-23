bool: a;

bool: b;

float: c;


constraint if a = true then b = true else c > 5 endif;

solve satisfy;


