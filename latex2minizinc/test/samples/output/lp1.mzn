var float: x;

var float: y;


constraint x + 2 * y <= 14;

constraint 3 * x - y >= 0;

constraint x - y <= 2;



var float: obj = 3 * x + 4 * y;

solve maximize obj;




