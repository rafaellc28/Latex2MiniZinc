var int: x1;

var int: x2;


constraint x1 >= 0;

constraint x2 >= 0;

constraint 1.85 * x1 + x2 <= 100;

constraint x1 + x2 <= 80;

constraint x1 <= 40;



var float: obj = 3 * x1 + 2 * x2;

solve maximize obj;




