int: budget = 10000;


var 0..1000: A = 0;

var 0..400: B = 0;

var 0..500: C = 0;

var 0..150: D;


constraint 13 * A + 21 * B + 17 * C + 90 * D <= budget;



solve maximize 6 * A + 10 * B + 8 * C + 40 * D;




