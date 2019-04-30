int: k = 4;


var 0..5: x;

var 0..2: y;

var 0..3: z;


constraint x + 2 * (y - x) + z <= k * z;

solve satisfy;


