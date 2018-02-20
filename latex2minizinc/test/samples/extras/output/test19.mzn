bool: a;

float: b;

bool: c;

float: d;


constraint if c = true then d else 0 endif <= 1;



solve maximize if a = true then b else 0 endif;




