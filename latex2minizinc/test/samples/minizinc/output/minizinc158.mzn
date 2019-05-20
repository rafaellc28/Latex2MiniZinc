var float: x;

var float: y;

var float: z;


constraint x >= 0;

constraint y >= 0;

constraint z >= 0;

constraint 2.0 * x + 2.0 * y + 1.0 * z <= 30.0;

constraint 1.5 * x + 2.0 * y + 3.0 * z <= 25.0;

constraint 2.0 * x + 1.0 * y + 1.0 * z <= 20.0;

constraint x <= 7;

constraint z <= 4;



solve maximize 3.0 * x + 1.0 * y + 3.0 * z;




