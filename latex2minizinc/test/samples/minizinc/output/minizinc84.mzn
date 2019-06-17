set of int: POST = 1..4;

set of int: PATH = 1..10;

array[POST] of int: guard;

array[PATH] of int: time;


var 0..2: weather;

var PATH: path;

var int: t = time[path] div weather + extra * weather;

var int: extra;


constraint path in POST -> extra = guard[path];

constraint not (path in POST) -> extra = 0;



solve minimize t;




