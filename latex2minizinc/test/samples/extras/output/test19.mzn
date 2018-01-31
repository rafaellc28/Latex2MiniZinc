float: a;

float: b;

float: c;

float: d;


constraint if c = true then d else 0 endif <= 1;



var float: obj = if a = true then b else 0 endif;

solve maximize obj;




