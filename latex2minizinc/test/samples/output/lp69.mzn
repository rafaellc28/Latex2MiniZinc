enum Sample;

array[int] of float: Sy;

array[int] of float: Sx;


var float: p;

var float: q;

var float: a;

var float: b;


constraint sum(z in Sample)(q * Sy[z] * Sy[z] + sum(z in Sample)(p * Sy[z])) = sum(z in Sample)(Sy[z] * Sx[z]);

constraint sum(z in Sample)(q * Sy[z] + sum(z in Sample)(p)) = sum(z in Sample)(Sx[z]);

constraint sum(z in Sample)(a * Sx[z] * Sx[z] + sum(z in Sample)(b * Sx[z])) = sum(z in Sample)(Sy[z] * Sx[z]);

constraint sum(z in Sample)(a * Sx[z] + sum(z in Sample)(b)) = sum(z in Sample)(Sy[z]);

solve satisfy;


