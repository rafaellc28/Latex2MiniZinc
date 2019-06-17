set of int: PATH = 1..10;

set of int: POST = 1..4;

array[PATH] of int: time;

array[POST] of int: guard;


var 0..2: weather;

var PATH: path;

var int: t = time[path] div weather + guard[path] * weather;






solve minimize t;




